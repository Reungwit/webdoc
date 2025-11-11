# views_chapter_3.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import json

from backend.models import DocChapter3
from django.http import HttpResponse, JsonResponse # เพิ่ม JsonResponse
from django.conf import settings
import io
import traceback # เพิ่ม traceback
from django.core.files.storage import default_storage # เพิ่ม default_storage

from man_doc.doc_chapter3 import doc_chapter3


# ---------------- JSON helpers (no leading underscore) ----------------
def parseMaybeJson(s):
    try:
        return json.loads(s)
    except Exception:
        return None

def coerceJsonList(v, default=None):
    if isinstance(v, list):
        return v
    if isinstance(v, str):
        s = v.strip()
        first = parseMaybeJson(s)
        if isinstance(first, list):
            return first
        if isinstance(first, str):
            second = parseMaybeJson(first)
            if isinstance(second, list):
                return second
    return list(default or [])

def coerceJsonObj(v, default=None):
    base = {"paragraphs": [], "items": [], "pictures": []}
    if isinstance(v, dict):
        base.update(v)
        base.setdefault("pictures", [])
        base.setdefault("paragraphs", [])
        base.setdefault("items", [])
        return base
    if isinstance(v, str):
        s = v.strip()
        first = parseMaybeJson(s)
        if isinstance(first, dict):
            base.update(first)
            base.setdefault("pictures", [])
            base.setdefault("paragraphs", [])
            base.setdefault("items", [])
            return base
        if isinstance(first, str):
            second = parseMaybeJson(first)
            if isinstance(second, dict):
                base.update(second)
                base.setdefault("pictures", [])
                base.setdefault("paragraphs", [])
                base.setdefault("items", [])
                return base
        if s:
            base["paragraphs"] = [s]
            return base
    d = dict(default or base)
    d.setdefault("pictures", [])
    d.setdefault("paragraphs", [])
    d.setdefault("items", [])
    return d

def readField(row, *names, default=None):
    if not row:
        return default
    for n in names:
        if hasattr(row, n):
            return getattr(row, n)
    return default

def putField(defaults: dict, name: str, value):
    if hasattr(DocChapter3, "_meta") and any(f.name == name for f in DocChapter3._meta.fields):
        defaults[name] = value


# ---------------- sections <-> tables splitter ----------------
def splitSectionsAndTables(sections):
    """
    รับ sections (list/dict ที่อาจมี 'tables' หรือ 'rows' ปะปน)
    คืนค่า (sections_clean, tables_found)
    - ลบคีย์ 'tables' และ 'rows' ทิ้งจาก sections
    - เก็บตารางทั้งหมดลง tables_found เป็น list
    รองรับรูปแบบซ้อนใน keys: mains, children, items
    """
    found_tables = []

    def clean(node):
        if isinstance(node, dict):
            node = dict(node)  # ทำสำเนา
            # ดึงตารางออกถ้ามี
            if "tables" in node and isinstance(node["tables"], list):
                found_tables.extend(node["tables"])
                node.pop("tables", None)
            if "rows" in node and isinstance(node["rows"], list):
                # เผื่อบาง UI ใส่ rows มาตรงๆ ให้ห่อเป็นตารางเดียว
                found_tables.append({"rows": node["rows"]})
                node.pop("rows", None)

            # เดินต่อในโครงสร้างที่เป็นลิสต์
            for k in ("mains", "children", "items"):
                if k in node and isinstance(node[k], list):
                    node[k] = [clean(x) for x in node[k]]
            return node

        if isinstance(node, list):
            return [clean(x) for x in node]
        return node

    cleaned = clean(sections)
    return cleaned, found_tables


# ---------------- View ----------------
@login_required
def chapter_3_view(request):
    user = request.user

    row = DocChapter3.objects.filter(user=user).order_by('-updated_at').first()

    db_intro_raw = readField(row, 'intro_body', default='')
    db_secs_raw  = readField(row, 'sections_json', default=[])
    db_tbls_raw  = readField(row, 'tb_sections_json', 'chapter3_tables_json', default=[])

    db_intro = coerceJsonObj(db_intro_raw, {"paragraphs": [], "items": [], "pictures": []})
    db_secs  = coerceJsonList(db_secs_raw, [])
    db_tbls  = coerceJsonList(db_tbls_raw, [])

    # ทำความสะอาด sections ที่อ่านมาจาก DB เผื่อมีตารางหลงเหลือ
    db_secs_clean, db_secs_tables = splitSectionsAndTables(db_secs)
    if db_secs_tables:
        # ผสานตารางที่พบเข้ากับของเดิม (ไม่ทำ DB write ทันที; จะบันทึกเมื่อ user กด save)
        db_tbls = db_tbls + db_secs_tables
        db_secs = db_secs_clean
    else:
        db_secs = db_secs_clean

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()

        intro_in_raw = request.POST.get('intro_body', '')
        secs_in_raw  = request.POST.get('sections_json', '')
        tbls_in_raw  = request.POST.get('tb_sections_json',
                           request.POST.get('chapter3_tables_json', ''))

        intro_in = coerceJsonObj(intro_in_raw, db_intro)
        secs_in  = coerceJsonList(secs_in_raw, db_secs)
        tbls_in  = coerceJsonList(tbls_in_raw, db_tbls)

        # >>> ตัด tables/rows ออกจาก sections และย้ายไป tb_sections_json <<<
        secs_clean, secs_tables = splitSectionsAndTables(secs_in)
        
        # [!] EDIT 1: ลบบรรทัดนี้ทิ้ง หรือ คอมเมนต์ออก เพื่อป้องกันตารางซ้ำซ้อน
        # if secs_tables:
        #     tbls_in = tbls_in + secs_tables
        
        secs_in = secs_clean

        if action == 'save':
            defaults = {'chap_id': 3, 'updated_at': timezone.now()}
            putField(defaults, 'intro_body', intro_in)
            putField(defaults, 'sections_json', secs_in)
            putField(defaults, 'tb_sections_json', tbls_in)
            putField(defaults, 'chapter3_tables_json', tbls_in)  # รองรับคอลัมน์เก่า

            DocChapter3.objects.update_or_create(user=user, defaults=defaults)

            messages.add_message(request, messages.SUCCESS, '💾 บันทึกข้อมูลบทที่ 3 เรียบร้อยแล้ว', extra_tags='chapter3')
            initial = {'intro_body': intro_in, 'sections': secs_in, 'tables': tbls_in}
            return render(request, 'chapter_3.html', {'initial': initial})

        if action == 'get_data':
            messages.add_message(request, messages.INFO, '🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว', extra_tags='chapter3')
            initial = {'intro_body': db_intro, 'sections': db_secs, 'tables': db_tbls}
            return render(request, 'chapter_3.html', {'initial': initial})

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
        
        
        if action in ('generate_doc', 'generate_docx'):
            media_root = getattr(settings, 'MEDIA_ROOT', '') or ''
            doc = doc_chapter3(
                intro_body=intro_in,
                sections_json=secs_in,      # ไม่มี tables/rows ปะปนแล้ว
                tables_json=tbls_in,        # ตารางทั้งหมดอยู่ที่นี่
                media_root=media_root,
            )
            buf = io.BytesIO()
            doc.save(buf)
            buf.seek(0)
            resp = HttpResponse(
                buf.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            resp['Content-Disposition'] = 'attachment; filename="chapter3.docx"'
            return resp

    # GET
    initial = {'intro_body': db_intro, 'sections': db_secs, 'tables': db_tbls}
    return render(request, 'chapter_3.html', {'initial': initial})