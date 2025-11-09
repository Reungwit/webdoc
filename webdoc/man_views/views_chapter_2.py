from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages

from io import BytesIO
import json, traceback

from backend.models import DocChapter2
from man_doc.doc_function import _safe_parse_list
from man_doc.doc_chapter2 import generate_doc


# ---------- Intro helpers (nested JSON) ----------
def intro_normalize(value):
    def clean_list(strings):
        return [str(s or "").strip() for s in (strings or []) if str(s or "").strip()]
    if isinstance(value, str):
        try:
            value = json.loads(value or "{}")
        except Exception:
            return {"paragraphs": clean_list((value or "").split("\n\n")), "subnodes": []}
    if isinstance(value, list):
        return {"paragraphs": clean_list(value), "subnodes": []}
    if isinstance(value, dict):
        paras = clean_list(value.get("paragraphs") or [])
        subs = []
        for it in (value.get("subnodes") or []):
            it = it or {}
            subs.append({
                "title": str(it.get("title") or "").strip(),
                "paragraphs": clean_list(it.get("paragraphs") or []),
            })
        return {"paragraphs": paras, "subnodes": subs}
    return {"paragraphs": [], "subnodes": []}


def intro_to_text(intro_dict, chapter_no="2"):
    data = intro_normalize(intro_dict)
    lines = []
    for p in data["paragraphs"]:
        lines.append(p)
    for i, sub in enumerate(data["subnodes"], start=1):
        head_no = f"{chapter_no}.{i}"
        title = (sub.get("title") or "").strip()
        lines.append(f"{head_no} {title}".strip())
        for para in (sub.get("paragraphs") or []):
            lines.append(para)
    return "\n\n".join([ln for ln in lines if str(ln).strip()])


@login_required
def chapter_2_view(request):
    user = request.user
    row = DocChapter2.objects.filter(user=user).first()

    intro_struct = intro_normalize(getattr(row, "intro_body", {}))
    sections_list = _safe_parse_list(getattr(row, "sections_json", []), [])

    if request.method == "GET":
        return render(request, "chapter_2.html", {
            "page_title": "บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง",
            "initial": {
                "intro_paras": intro_struct,
                "sections": sections_list,
            }
        })

    action = (request.POST.get('action') or '').strip()

    if action == 'get_data':
        return redirect(request.path)

    if action == 'save':
        intro_raw = request.POST.get('intro_body', '{}')
        intro_data = intro_normalize(intro_raw)

        sections_raw = request.POST.get('sections_json', '[]')
        sections_data = _safe_parse_list(sections_raw, [])

        try:
            DocChapter2.objects.update_or_create(
                user=request.user,
                defaults={
                    'chap_id': 2,
                    'intro_body': intro_data,
                    'sections_json': sections_data,
                    'updated_at': timezone.now(),
                }
            )
            messages.success(request, 'บันทึกข้อมูลสำเร็จ ✅')
        except IntegrityError as e:
            messages.error(request, f'IntegrityError: {e}')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect(request.path)

    if action == 'add_picture':
        # บริการอัปโหลดรูปจาก JS + คืนข้อมูลรูป (สะท้อน pic_no กลับไปด้วย)
        try:
            pic_name = (request.POST.get('pic_name') or '').strip()
            pic_no   = (request.POST.get('pic_no') or '').strip()   # 2-1, 2-2, ...
            upfile   = request.FILES.get('pic_file')
            if not upfile:
                return JsonResponse({'status': 'error', 'message': 'ไม่พบไฟล์ (pic_file)'}, status=400)

            user_path = f'img/user_{request.user.username}/{upfile.name}'
            saved_path = default_storage.save(user_path, upfile)
            saved_url  = default_storage.url(saved_path)

            picture_block = {
                "pic_no": pic_no,        # <<-- สำคัญ: ส่งกลับให้แสดง “ภาพที่ 2-x”
                "pic_name": pic_name,
                "pic_path": saved_path,
                "pic_url": saved_url,
                "captions": [],
            }
            return JsonResponse({"status": "ok", "message": "อัปโหลดรูปสำเร็จ", "picture": picture_block})
        except Exception:
            return JsonResponse(
                {'status': 'error', 'message': 'Upload failed', 'trace': traceback.format_exc()},
                status=500
            )

    if action == "generate_doc":
        try:
            intro_text = intro_to_text(request.POST.get('intro_body', '{}'), chapter_no="2")
            sections = _safe_parse_list(request.POST.get('sections_json', '[]'), [])

            def extract_all_pictures(sections_list):
                pics = []
                def walk(node):
                    if not isinstance(node, dict): return
                    if isinstance(node.get("pictures"), list):
                        pics.extend([p for p in node["pictures"] if p])
                    for ch in (node.get("children") or []):
                        walk(ch)
                if isinstance(sections_list, list):
                    for sec in sections_list:
                        if not isinstance(sec, dict): continue
                        if isinstance(sec.get("pictures"), list):
                            pics.extend([p for p in sec["pictures"] if p])
                        for nd in (sec.get("items") or []):
                            walk(nd)
                return pics

            all_pics = extract_all_pictures(sections)

            doc = generate_doc(
                intro_body=intro_text,
                sections_json=sections,
                pictures=all_pics,
                media_root=settings.MEDIA_ROOT,
            )
            bio = BytesIO(); doc.save(bio); bio.seek(0)
            resp = FileResponse(
                bio, as_attachment=True, filename="chapter2.docx",
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            resp["Cache-Control"] = "no-store"
            return resp
        except Exception:
            messages.error(request, f'Generate failed: {traceback.format_exc()}')
            return redirect(request.path)

    messages.error(request, f'unknown action \"{action}\"')
    return redirect(request.path)
