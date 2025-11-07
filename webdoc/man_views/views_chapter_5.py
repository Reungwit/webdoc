# -*- coding: utf-8 -*-
# backend/man_views/views_chapter_5.py

from __future__ import annotations
import json
from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render
from django.utils import timezone

# NOTE: ถ้าวางไฟล์นี้ใน backend/views.py ให้เปลี่ยนเป็น "from .models import Chapter5"
from backend.models import Chapter5

# ตัวสร้างเอกสารบทที่ 5
from man_doc.doc_chapter5 import doc_chapter5

# ฟังก์ชันกลาง: แปลง schema จาก UI -> schema คงที่สำหรับเอกสาร
from man_doc.doc_function import sections_db_from_ui


# ---------------- ค่ามาตรฐาน/ตัวช่วย ----------------
DEFAULT_TITLES = ['สรุปผลการดำเนินงาน', 'อภิปรายผล', 'ข้อเสนอแนะ']


def _one_paragraph(text: str) -> str:
    """แปลงข้อความให้เป็น 'ย่อหน้าเดียว' (ตัดบรรทัดใหม่/รวมช่องว่าง)"""
    if not isinstance(text, str):
        return ''
    return ' '.join(text.replace('\r\n', '\n').split())


def _build_ch5_document(doc_ch5_func, intro_body, sections_for_doc):
    """
    Adapter เรียก doc_chapter5 ให้สำเร็จ แม้ signature ในเครื่องจะต่างกัน
    รองรับ:
      1) doc_chapter5(intro_body, sections_json)           # เวอร์ชันใหม่ (แนะนำ)
      2) doc_chapter5(sections_json)                       # เวอร์ชันเก่า
      3) doc_chapter5(sections_json, intro_body=...)       # บางโปรเจ็กต์ดัดแปลง
      4) doc_chapter5(intro_body=intro_body, sections_json=sections_for_doc)  # keyword
    """
    # 1) ใหม่: 2 positional
    try:
        return doc_ch5_func(intro_body, sections_for_doc)
    except TypeError:
        pass

    # 2) เก่า: 1 positional
    try:
        return doc_ch5_func(sections_for_doc)
    except TypeError:
        pass

    # 3) แปลก: sections_json เป็น pos, intro_body เป็น kw
    try:
        return doc_ch5_func(sections_for_doc, intro_body=intro_body)
    except TypeError:
        pass

    # 4) keyword ล้วน
    try:
        return doc_ch5_func(intro_body=intro_body, sections_json=sections_for_doc)
    except TypeError:
        # สุดท้ายลองแบบ sections_json อย่างเดียว
        return doc_ch5_func(sections_json=sections_for_doc)


# ---------------- View หลักของบทที่ 5 ----------------
@login_required
def chapter_5_view(request):
    """
    หน้าฟอร์ม/บันทึก/ดึงข้อมูล/สร้าง DOCX สำหรับ 'บทที่ 5'
    - บทนำ: ย่อหน้าเดียว (ไม่มีเลขหัวข้อ)
    - หัวข้อมีเลข: 5.1 สรุปผลการดำเนินงาน, 5.2 อภิปรายผล, 5.3 ข้อเสนอแนะ
    - ใช้ sections_db_from_ui() เป็นฟังก์ชันกลาง normalize โครงสร้างจาก UI
    """
    user = request.user

    # ดึงค่าล่าสุดจาก DB (ถ้ามี)
    row = Chapter5.objects.filter(user=user).order_by('-updated_at').first()
    db_intro = (row.intro_th if row else '') or ''
    db_sections = row.sections_json if (row and isinstance(row.sections_json, list)) else []

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()
        intro_body = _one_paragraph(request.POST.get('intro_body') or '')
        raw_json = request.POST.get('chapter5_json', '')

        # ---------- บันทึกข้อมูล ----------
        if action == 'save':
            try:
                sections_in = json.loads(raw_json or '[]')
                if not isinstance(sections_in, list):
                    sections_in = []
            except json.JSONDecodeError:
                sections_in = []

            Chapter5.objects.update_or_create(
                user=user,
                defaults={
                    'intro_th': intro_body,
                    'sections_json': sections_in,    # เก็บตาม schema UI ที่ส่งมา
                    'updated_at': timezone.now(),
                }
            )
            messages.success(request, '💾 บันทึกข้อมูลบทที่ 5 เรียบร้อยแล้ว')
            return render(request, 'chapter_5.html', {
                'initial': {'intro_body': '', 'chapter5_json': []}
            })

        # ---------- ดึงข้อมูลล่าสุดกลับไปเติมฟอร์ม ----------
        elif action == 'get_data':
            messages.info(request, '🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว')
            return render(request, 'chapter_5.html', {
                'initial': {'intro_body': db_intro, 'chapter5_json': db_sections}
            })

        # ---------- สร้าง DOCX ----------
        elif action == 'generate_docx':
            # ถ้าไม่ได้กรอกบทนำในคำขอล่าสุด ให้ fallback เป็นค่าจาก DB
            if not intro_body:
                intro_body = _one_paragraph(db_intro)

            # Normalize โครงสร้างจาก UI -> โครงสร้างคงที่ที่ตัวสร้างเอกสารต้องการ
            sections_for_doc = sections_db_from_ui(
                raw_json or db_sections,           # รับได้ทั้ง JSON สตริงและ list
                default_titles=DEFAULT_TITLES,     # บังคับลำดับ 5.1–5.3
                first_section_mode='paragraphs',   # บทนำเป็น 'paragraphs' (ไม่มีเลขหัวข้อ)
            )

            # ใช้ adapter เพื่อกัน signature ของ doc_chapter5 ไม่ตรง
            doc = _build_ch5_document(doc_chapter5, intro_body, sections_for_doc)

            # ส่งไฟล์ให้ดาวน์โหลด
            buf = BytesIO()
            doc.save(buf)
            buf.seek(0)
            return FileResponse(
                buf,
                as_attachment=True,
                filename='chapter5.docx',
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

        # ---------- คำสั่งอื่น ๆ ----------
        messages.info(request, 'ยังไม่รองรับการทำงานนี้')
        return render(request, 'chapter_5.html', {
            'initial': {'intro_body': '', 'chapter5_json': []}
        })

    # ---------- GET: เปิดฟอร์มครั้งแรก ----------
    return render(request, 'chapter_5.html', {
        'initial': {
            'intro_body': (db_intro if (db_intro or db_sections) else ''),
            'chapter5_json': (db_sections if isinstance(db_sections, list) else []),
        }
    })
