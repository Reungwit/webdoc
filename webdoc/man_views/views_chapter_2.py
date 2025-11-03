from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError, transaction
import json

from backend.models import DocChapter2  # ต้องอ้างโมเดลบทที่ 2 ของคุณจริง ๆ

# 1. (เพิ่ม Import) เราต้องการตัวจัดการไฟล์ของ Django
from django.core.files.storage import default_storage


@login_required
def chapter_2_view(request):
    user = request.user  # CustomUser ของคุณ

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()

        # ---------- ดึงข้อมูล (ไม่ได้แก้ไข) ----------
        if action == 'get_data':
            row = DocChapter2.objects.filter(user=user).first()
            if row:
                return JsonResponse({
                    'initial': {
                        'intro_body': row.intro_body or "",
                        'sections': row.sections_json or [],
                    }
                })
            else:
                return JsonResponse({
                    'initial': {
                        'intro_body': "",
                        'sections': [],
                    }
                })

        # ---------- บันทึก (ไม่ได้แก้ไข) ----------
        if action == 'save':
            intro_body = request.POST.get('intro_body', '')

            raw_sections = request.POST.get('sections_json', '[]')
            try:
                sections_data = json.loads(raw_sections)
                if not isinstance(sections_data, list):
                    sections_data = []
            except json.JSONDecodeError:
                sections_data = []

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
            except IntegrityError as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'IntegrityError: {e}'
                }, status=400)
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error: {e}'
                }, status=400)

            return JsonResponse({'status': 'ok'})

        # ---------- generate_doc (ไม่ได้แก้ไข) ----------
        if action == 'generate_doc':
            return JsonResponse({
                'status': 'ok',
                'message': 'สร้างเอกสารเสร็จ (mock)'
            })

        # ---------- add_picture (ส่วนที่แก้ไข) ----------
        if action == 'add_picture':
            try:
                # 1. ดึงข้อมูลจาก request
                pic_name  = request.POST.get('pic_name', '').strip()
                client_pic_no = request.POST.get('pic_no', '') # เลขที่ JS ส่งมา
                upfile    = request.FILES.get('pic_file')

                if not upfile:
                    return JsonResponse({'status': 'error', 'message': 'ไม่พบไฟล์ (pic_file)'}, status=400)

                # 2. สร้าง Path ที่คุณต้องการ
                file_name = upfile.name
                
                # !! [แก้ไข] เปลี่ยนจาก .pk เป็น .username !!
                # โค้ดเดิม: user_specific_path = f'img/user_{request.user.pk}/{file_name}'
                user_specific_path = f'img/user_{request.user.username}/{file_name}'

                # 3. บันทึกไฟล์ลง Storage (MEDIA_ROOT)
                saved_relative_path = default_storage.save(user_specific_path, upfile)

                # 4. (เผื่อใช้) ดึง URL เต็ม
                saved_url = default_storage.url(saved_relative_path)

                # 5. เตรียมข้อมูลส่งกลับให้ JS
                picture_block = {
                    "pic_no": client_pic_no,
                    "pic_name": pic_name,
                    "pic_path": saved_relative_path,
                    "pic_url": saved_url
                }

                return JsonResponse({
                    "status": "ok",
                    "message": "อัปโหลดรูปสำเร็จ",
                    "picture": picture_block
                })

            except Exception as e:
                # 6. ดักจับข้อผิดพลาด
                return JsonResponse({'status': 'error', 'message': f'Upload failed: {str(e)}'}, status=500)


        # ไม่รู้จัก action (ไม่ได้แก้ไข)
        return JsonResponse(
            {'status': 'error', 'message': f'unknown action "{action}"'},
            status=400
        )

        # ----------------- unknown action -----------------
        return JsonResponse({"status": "error", "message": f"ไม่รู้จัก action: {action}"})

    # GET: render หน้า (ไม่ได้แก้ไข)
    return render(request, "chapter_2.html", {
        "page_title": "บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง"
    })