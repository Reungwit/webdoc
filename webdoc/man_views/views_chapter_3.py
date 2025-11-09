# man_views/views_chapter_3.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
<<<<<<< HEAD
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import json
import os
import datetime
=======
import json
>>>>>>> cdafcf3a0d75cabfe6883792e0957eeeeefffc29

from backend.models import DocChapter3


def safe_parse_list(raw_text, fallback):
    """
    แปลง string JSON -> list อย่างปลอดภัย
<<<<<<< HEAD
    raw_text: ข้อมูลจาก <input type="hidden"> ที่หน้าเว็บส่งมา (เช่น sections_json / chapter3_tables_json)
=======
    raw_text: ข้อมูลจาก <textarea> (เช่น chapter3_json)
>>>>>>> cdafcf3a0d75cabfe6883792e0957eeeeefffc29
    fallback: ค่าจาก DB (list) เมื่อ parse ไม่สำเร็จ
    """
    try:
        data = json.loads(raw_text or '[]')
        return data if isinstance(data, list) else (fallback or [])
    except json.JSONDecodeError:
        return fallback or []


@login_required
def chapter_3_view(request):
    user = request.user

<<<<<<< HEAD
    # อ่านข้อมูลล่าสุดจาก DB ของผู้ใช้คนนี้
    row = DocChapter3.objects.filter(user=user).order_by('-updated_at').first()
    db_intro   = (row.intro_body if row else '') or ''
    db_secs    = row.sections_json    if (row and isinstance(row.sections_json, list))    else []
    db_tables  = row.tb_sections_json if (row and isinstance(row.tb_sections_json, list)) else []

    # ============ POST ============
    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()

        # ---------- AJAX: add_picture ----------
        if action == 'add_picture':
            """
            ฝั่ง JS จะส่ง:
              - node_no    (ใช้เป็น anchor อ้างกับ UI)
              - pic_name   (ชื่อ/คำอธิบายรูป)
              - pic_path   (ชื่อไฟล์เดิมสำหรับโชว์ใน UI)
              - pic_no     (เลขภาพ เช่น 3-1, 3-2 ... JS คำนวณให้แล้ว)
              - pic_file   (ไฟล์จริง)
            เราจะบันทึกไฟล์ลง default_storage แล้วตอบ JSON กลับ
            """
            pic_name = (request.POST.get('pic_name') or '').strip()
            pic_no   = (request.POST.get('pic_no')   or '').strip()
            upload   = request.FILES.get('pic_file')

            if not upload or not pic_name:
                return JsonResponse(
                    {'ok': False, 'message': 'ข้อมูลรูปภาพไม่ครบ'},
                    status=400
                )

            # สร้าง path เก็บไฟล์: img/user_<id>/chapter3/<YYYYMMDD_HHMMSS>_<orig>
            ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            base_dir = f'img/user_{user.pk}/chapter3'
            filename = f'{ts}_{upload.name}'
            rel_path = os.path.join(base_dir, filename).replace('\\', '/')

            saved_path = default_storage.save(rel_path, ContentFile(upload.read()))
            file_url   = default_storage.url(saved_path)

            payload = {
                'ok': True,
                'message': 'อัปโหลดสำเร็จ',
                'picture': {
                    'pic_no': pic_no,
                    'pic_name': pic_name,
                    # เก็บ path/url สำหรับโชว์กลับในหน้า
                    'pic_path': file_url,
                    'server_pic_no': pic_no,
                }
            }
            return JsonResponse(payload, status=200)

        # ---------- ปกติ: save / get_data / generate_doc ----------
        intro_body   = (request.POST.get('intro_body') or '').strip()

        # ชื่อฟิลด์ตาม template ปัจจุบัน
        raw_secs     = request.POST.get('sections_json', '')
        raw_tables   = request.POST.get('chapter3_tables_json', '')

        if action == 'save':
            secs_in   = safe_parse_list(raw_secs, db_secs)
            tables_in = safe_parse_list(raw_tables, db_tables)

            DocChapter3.objects.update_or_create(
                user=user,
                defaults={
                    'intro_body'      : intro_body,
                    'sections_json'   : secs_in,
                    'tb_sections_json': tables_in,
                    'chap_id'         : 3,
                    'updated_at'      : timezone.now(),
                }
            )
            messages.success(request, '💾 บันทึกข้อมูลบทที่ 3 เรียบร้อยแล้ว', extra_tags='chapter3')
            return render(request, 'chapter_3.html', {
                'initial': {
                    'intro_body': intro_body,
                    # ส่งคีย์ที่ template รอใช้งานจริง
                    'sections' : secs_in,
                    'tables'   : tables_in,
=======
    # อ่านของเดิมจาก DB แถวล่าสุด (ต่อ user)
    row = DocChapter3.objects.filter(user=user).order_by('-updated_at').first()
    db_intro = (row.intro_body if row else '') or ''
    db_secs = row.sections_json if (row and isinstance(row.sections_json, list)) else []
    db_tables = row.tb_sections_json if (row and isinstance(row.tb_sections_json, list)) else []

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()
        intro_body = (request.POST.get('intro_body') or '').strip()
        raw_secs = request.POST.get('chapter3_json', '')
        raw_tables = request.POST.get('chapter3_tables_json', '')

        if action == 'save':
            secs_in = safe_parse_list(raw_secs, db_secs)
            tables_in = safe_parse_list(raw_tables, db_tables)

            DocChapter3.objects.update_or_create(
                user=user,
                defaults={
                    'intro_body': intro_body,
                    'sections_json': secs_in,
                    'tb_sections_json': tables_in,
                    'chap_id': 3,
                    'updated_at': timezone.now(),
                }
            )
            messages.success(request, '💾 บันทึกข้อมูลบทที่ 3 เรียบร้อยแล้ว')
            return render(request, 'chapter_3.html', {
                'initial': {
                    'intro_body': intro_body,
                    'chapter3_json': secs_in,
                    'chapter3_tables_json': tables_in,
>>>>>>> cdafcf3a0d75cabfe6883792e0957eeeeefffc29
                }
            })

        elif action == 'get_data':
<<<<<<< HEAD
            messages.info(request, '🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว', extra_tags='chapter3')
            return render(request, 'chapter_3.html', {
                'initial': {
                    'intro_body': db_intro,
                    'sections'  : db_secs,
                    'tables'    : db_tables,
                }
            })

        elif action == 'generate_doc':
            # ตรงนี้คุณผูกกับตัว generator ของคุณเองได้ตามเดิม
            messages.info(request, 'ยังไม่รองรับการสร้างเอกสารในส่วนนี้', extra_tags='chapter3')
            return render(request, 'chapter_3.html', {
                'initial': {
                    'intro_body': db_intro,
                    'sections'  : db_secs,
                    'tables'    : db_tables,
                }
            })

        # อื่น ๆ
        messages.info(request, 'ยังไม่รองรับการทำงานนี้', extra_tags='chapter3')
        return render(request, 'chapter_3.html', {
            'initial': {
                'intro_body': db_intro,
                'sections'  : db_secs,
                'tables'    : db_tables,
            }
        })

    # ============ GET ============
    return render(request, 'chapter_3.html', {
        'initial': {
            'intro_body': db_intro,
            'sections'  : db_secs,
            'tables'    : db_tables,
=======
            messages.info(request, '🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว')
            return render(request, 'chapter_3.html', {
                'initial': {
                    'intro_body': db_intro,
                    'chapter3_json': db_secs,
                    'chapter3_tables_json': db_tables,
                }
            })

        # เผื่อ action อื่นในอนาคต (เช่น generate_docx)
        messages.info(request, 'ยังไม่รองรับการทำงานนี้')
        return render(request, 'chapter_3.html', {
            'initial': {
                'intro_body': db_intro,
                'chapter3_json': db_secs,
                'chapter3_tables_json': db_tables,
            }
        })

    # GET
    return render(request, 'chapter_3.html', {
        'initial': {
            'intro_body': db_intro,
            'chapter3_json': db_secs,
            'chapter3_tables_json': db_tables,
>>>>>>> cdafcf3a0d75cabfe6883792e0957eeeeefffc29
        }
    })
