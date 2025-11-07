# man_views/views_chapter_3.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import json

from backend.models import DocChapter3


def safe_parse_list(raw_text, fallback):
    """
    แปลง string JSON -> list อย่างปลอดภัย
    raw_text: ข้อมูลจาก <textarea> (เช่น chapter3_json)
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
                }
            })

        elif action == 'get_data':
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
        }
    })
