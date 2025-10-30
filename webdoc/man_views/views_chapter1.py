from django.shortcuts import render
from django.http import FileResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import json
from io import BytesIO

from backend.models import DocChapter1  # ← ต้องมีใน models.py
from man_doc.doc_chapter1 import doc_chapter1  # ← ตัว generator .docx ของบทที่ 1


def _safe_parse_list(raw_text, fallback):
    """
    raw_text: string JSON จาก <input type="hidden" name="chapter1_json">
    fallback: list (ค่าที่อ่านมาจาก DB แล้ว parse สำเร็จ)
    return: list พร้อมใช้งาน
    """
    try:
        data = json.loads(raw_text or '[]')
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass
    return fallback or []


@login_required
def chapter_1_view(request):
    """
    View บทที่ 1 (เวอร์ชันใหม่แบบ dynamic)
    ใช้ตาราง doc_chapter_1 ผ่านโมเดล DocChapter1
    workflow เหมือนบทที่ 5: save / get_data / generate_docx
    """
    user = request.user

    # ดึงข้อมูลล่าสุดของ user นี้ถ้ามี
    row = DocChapter1.objects.filter(user=user).order_by('-updated_at').first()

    # intro_th เก็บบทนำ (ย่อหน้าเปิดบทที่ 1)
    db_intro = (row.intro_th if row else '') or ''

    # sections_json เก็บเป็น LONGTEXT (string JSON) ใน DB
    # เราจะแปลงเป็น list เพื่อส่งไป template
    db_sections_list = []
    if row and row.sections_json:
        try:
            tmp = json.loads(row.sections_json)
            if isinstance(tmp, list):
                db_sections_list = tmp
        except Exception:
            db_sections_list = []

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()

        intro_body = (request.POST.get('intro_body') or '').strip()
        raw_json   = request.POST.get('chapter1_json', '')

        sections_from_form = _safe_parse_list(raw_json, db_sections_list)

        # -------- บันทึกข้อมูล --------
        if action == 'save':
            sections_str = json.dumps(sections_from_form, ensure_ascii=False)

            DocChapter1.objects.update_or_create(
                user=user,
                defaults={
                    'intro_th': intro_body,
                    'sections_json': sections_str,
                    'updated_at': timezone.now(),
                }
            )

            messages.success(request, '💾 บันทึกข้อมูลบทที่ 1 เรียบร้อยแล้ว')
            return render(request, 'chapter_1.html', {
                'initial': {
                    'intro_body': '',
                    'chapter1_json': []
                }
            })

        # -------- ดึงข้อมูลกลับมาแสดง --------
        elif action == 'get_data':
            messages.info(request, '🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว')
            return render(request, 'chapter_1.html', {
                'initial': {
                    'intro_body': db_intro,
                    'chapter1_json': db_sections_list
                }
            })

        # -------- สร้างเอกสาร docx --------
        elif action == 'generate_docx':
            # ถ้า intro_body ว่างจากฟอร์ม เรา fallback ไปใช้ค่าที่ใน DB
            if not intro_body:
                intro_body = db_intro

            # sections สำหรับส่งเข้า doc builder
            sections_for_doc = sections_from_form if sections_from_form else db_sections_list

            # NOTE: ต้องปรับ doc_chapter1() ให้รับ (intro_body, sections_for_doc)
            # และ return เป็น python-docx Document()
            doc = doc_chapter1(intro_body, sections_for_doc)

            buf = BytesIO()
            doc.save(buf)
            buf.seek(0)
            return FileResponse(
                buf,
                as_attachment=True,
                filename='chapter1.docx',
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

        # action ไม่ตรง
        messages.info(request, 'ยังไม่รองรับการทำงานนี้')
        return render(request, 'chapter_1.html', {
            'initial': {
                'intro_body': '',
                'chapter1_json': []
            }
        })

    # -------- GET ปกติ (เข้าหน้าเฉย ๆ) --------
    return render(request, 'chapter_1.html', {
        'initial': {
            # ใส่ intro_body ถ้ามีข้อมูลแล้ว
            'intro_body': (db_intro if (db_intro or db_sections_list) else ''),
            # sections ที่ parse เป็น list แล้ว (ถ้าไม่มีเลย template จะ fallback defaultSections)
            'chapter1_json': db_sections_list,
        }
    })
