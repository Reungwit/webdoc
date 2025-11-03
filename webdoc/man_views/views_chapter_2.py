from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError, transaction
import json

from backend.models import DocChapter2  # ต้องอ้างโมเดลบทที่ 2 ของคุณจริง ๆ


@login_required
def chapter_2_view(request):
    user = request.user  # CustomUser ของคุณ

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()

        # ---------- ดึงข้อมูล ----------
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

        # ---------- บันทึก ----------
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

        # ---------- generate_doc ----------
        if action == 'generate_doc':
            return JsonResponse({
                'status': 'ok',
                'message': 'สร้างเอกสารเสร็จ (mock)'
            })

        # ---------- add_picture ----------
        if action == 'add_picture':
            node_no   = request.POST.get('node_no', '').strip()
            pic_name  = request.POST.get('pic_name', '').strip()
            client_fn = request.POST.get('pic_path', '').strip()
            upfile    = request.FILES.get('pic_file')

            pseudo_pic_no = f"{node_no}-1"

            picture_block = {
                "pic_no": pseudo_pic_no,
                "pic_name": pic_name,
                "pic_path": client_fn or (upfile.name if upfile else ''),
            }

            return JsonResponse({
                "status": "ok",
                "message": "เพิ่มรูปสำเร็จ",
                "picture": picture_block
            })

        # ไม่รู้จัก action
        return JsonResponse(
            {'status': 'error', 'message': f'unknown action "{action}"'},
            status=400
        )

        # ----------------- unknown action -----------------
        return JsonResponse({"status": "error", "message": f"ไม่รู้จัก action: {action}"})

    # GET: render หน้า
    return render(request, "chapter_2.html", {
        "page_title": "บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง"
    })