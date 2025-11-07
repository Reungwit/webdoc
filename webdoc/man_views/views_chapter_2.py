# views_chapter_2.py

from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.conf import settings
from django.core.files.storage import default_storage
from io import BytesIO
import json, traceback
from django.contrib import messages
from man_doc.doc_function import _safe_parse_list
from backend.models import DocChapter2
from man_doc.doc_chapter2 import generate_doc

@login_required
def chapter_2_view(request):
    user = request.user
    row = DocChapter2.objects.filter(user=user).first()
    db_intro = (getattr(row, "intro_body", "") or "")
    db_sections_raw = getattr(row, "sections_json", [])
    
    db_sections = _safe_parse_list(db_sections_raw, [])

    # ===== GET (ปรับปรุงใหม่) =====
    if request.method == "GET":
        return render(request, "chapter_2.html", {
            "page_title": "บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง",
            "initial": {
                "intro_body": db_intro,
                "sections": db_sections,
            }
        })

    # ===== POST (จัดการทุก action) =====
    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()
        if action == 'get_data':
            # ไม่ต้องทำอะไร ปล่อยให้ redirect กลับไปหน้า GET
            # ซึ่งหน้า GET จะดึงข้อมูลล่าสุดจาก DB มาแสดงเอง
            return redirect(request.path)

        # --- บันทึกข้อมูล (ปรับปรุงเล็กน้อย) ---
        if action == 'save':
            intro_body = request.POST.get('intro_body', '')
            raw_sections = request.POST.get('sections_json', '[]')
            sections_data = _safe_parse_list(raw_sections, [])

            try:
                DocChapter2.objects.update_or_create(
                    user=request.user,
                    defaults={
                        'chap_id': 2,
                        'intro_body': intro_body,
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

        # --- เพิ่มรูปภาพ (คงเดิม ไม่เปลี่ยนแปลง) ---
        if action == 'add_picture':
            try:
                pic_name = request.POST.get('pic_name', '').strip()
                client_pic_no = request.POST.get('pic_no', '').strip()
                upfile = request.FILES.get('pic_file')
                if not upfile:
                    return JsonResponse({'status': 'error', 'message': 'ไม่พบไฟล์ (pic_file)'}, status=400)
                
                user_specific_path = f'img/user_{request.user.username}/{upfile.name}'
                saved_relative_path = default_storage.save(user_specific_path, upfile)
                saved_url = default_storage.url(saved_relative_path)
                
                picture_block = {
                    "pic_no": client_pic_no,
                    "pic_name": pic_name,
                    "pic_path": saved_relative_path,
                    "pic_url": saved_url
                }
                return JsonResponse({"status": "ok", "message": "อัปโหลดรูปสำเร็จ", "picture": picture_block})
            except Exception:
                return JsonResponse(
                    {'status': 'error', 'message': 'Upload failed', 'trace': traceback.format_exc()},
                    status=500
                )

        # --- สร้างเอกสาร (ปรับปรุงเล็กน้อย) ---
        if action == "generate_doc":
            try:
                intro = request.POST.get('intro_body', '')
                raw_sections_json = request.POST.get('sections_json', '[]')
                
                # 7. [ปรับปรุง] เรียกใช้ฟังก์ชันกลาง _safe_parse_list
                sections = _safe_parse_list(raw_sections_json, [])
                
                # (ส่วน logic ของ extractAllPictures คงเดิม เพราะเป็น logic เฉพาะของบทที่ 2)
                def extractAllPictures(sections_list):
                    pics = []
                    def walkNode(node):
                        if not isinstance(node, dict): return
                        if isinstance(node.get("pictures"), list):
                            pics.extend([p for p in node["pictures"] if p])
                        if isinstance(node.get("children"), list):
                            for ch in node["children"]:
                                walkNode(ch)
                    if isinstance(sections_list, list):
                        for sec in sections_list:
                            if not isinstance(sec, dict): continue
                            if isinstance(sec.get("pictures"), list):
                                pics.extend([p for p in sec["pictures"] if p])
                            if isinstance(sec.get("items"), list):
                                for node in sec["items"]:
                                    walkNode(node)
                    def seq(p):
                        try:
                            return int(str(p.get("pic_no","0-0")).split("-")[-1])
                        except Exception:
                            return 0
                    pics.sort(key=seq)
                    return pics

                all_pics = extractAllPictures(sections)

                doc = generate_doc(
                    intro_body=intro,
                    sections_json=sections,
                    pictures=all_pics,
                    media_root=settings.MEDIA_ROOT,
                )
                
                bio = BytesIO()
                doc.save(bio)
                bio.seek(0)
                resp = FileResponse(
                    bio,
                    as_attachment=True,
                    filename="chapter2.docx",
                    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
                resp["Cache-Control"] = "no-store"
                return resp
                
            except Exception:
                messages.error(request, f'Generate failed: {traceback.format_exc()}')
                return redirect(request.path)

        # ไม่รู้จัก action
        messages.error(request, f'unknown action "{action}"')
        return redirect(request.path)