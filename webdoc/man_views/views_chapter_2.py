# man_views/views_chapter_2.py
import json
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.db import transaction
from django.conf import settings

from backend.models import DocChapter2  # ← ใช้แค่ตารางนี้ตามฐานข้อมูลใหม่

# ฟังก์ชันกลางจาก doc_function (ไฟล์ของคุณ)
try:
    from man_doc.doc_function import sections_ui_from_db, sections_db_from_ui
except ImportError:
    # fallback กรณี path ต่างจากโปรเจกต์จริง
    from doc_function import sections_ui_from_db, sections_db_from_ui  # noqa

@login_required
@require_http_methods(["GET", "POST"])
@transaction.atomic
def chapter_2_view(request):
    user = request.user  # AUTH_USER_MODEL

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()

        # -------------------- 1) ดึงข้อมูลกลับมาแสดง --------------------
        if action == "get_data":
            try:
                doc = DocChapter2.objects.get(user=user)
                initial = {
                    "intro_body": doc.intro_body or "",
                    # แปลง schema DB -> UI เพื่อยิงเข้า template initial
                    "sections": sections_ui_from_db(doc.sections_json, first_section_mode="body"),
                    "pics": doc.pic_data_json or [],  # รายการรูปในบทนี้ (จัดเก็บในคอลัมน์เดียว)
                }
                return JsonResponse({"status": "ok", "initial": initial})
            except DocChapter2.DoesNotExist:
                # เคสยังไม่มีข้อมูล ให้ initial เปล่า ๆ
                return JsonResponse({
                    "status": "nodata",
                    "initial": {
                        "intro_body": "",
                        "sections": sections_ui_from_db(None, first_section_mode="body"),
                        "pics": [],
                    }
                })

        # -------------------- 2) บันทึก/อัปเดตข้อมูล --------------------
        elif action == "save":
            intro_body = request.POST.get("intro_body", "")
            sections_raw = request.POST.get("sections_json", "[]")

            # UI -> DB (คงโครงสร้าง mains ให้ใช้ได้ทุกบท)
            sections_for_db = sections_db_from_ui(sections_raw, first_section_mode="body")

            # อัปเดต/สร้างใหม่ แยกตาม user_id
            obj, created = DocChapter2.objects.update_or_create(
                user=user,
                defaults={
                    "intro_body": intro_body,
                    "sections_json": sections_for_db,
                    "chap_no": 2,                 # เก็บเลขบทตามเส้นทาง chapter_2/
                    # ไม่แตะ pic_data_json ที่มีอยู่ (ปล่อยให้เดิมอยู่)
                }
            )
            return JsonResponse({"status": "ok", "message": "บันทึกข้อมูลบทที่ 2 สำเร็จ"})

        # -------------------- 3) แนบรูป (เก็บลงคอลัมน์ pic_data_json) --------------------
        elif action == "add_picture":
            pic_name = (request.POST.get("pic_name") or "").strip()
            pic_file = request.FILES.get("pic_file")

            if not pic_name:
                return JsonResponse({"status": "error", "message": "กรุณากรอกชื่อรูป"})
            if not pic_file:
                return JsonResponse({"status": "error", "message": "กรุณาแนบไฟล์รูปภาพ"})

            # ให้แน่ใจว่ามีแถวของบทที่ 2 ก่อน
            doc, _ = DocChapter2.objects.get_or_create(
                user=user,
                defaults={
                    "intro_body": "",
                    "sections_json": [],
                    "pic_data_json": [],
                    "chap_no": 2,
                }
            )

            # จัดเก็บไฟล์ลง storage
            upload_dir = os.path.join("user_uploads", f"user_{getattr(user, 'user_id', user.pk)}", "chap_2")
            file_name = default_storage.get_available_name(os.path.join(upload_dir, pic_file.name))
            saved_path = default_storage.save(file_name, pic_file)

            # สร้างหมายเลขรูปแบบ 2-ลำดับ
            pics = list(doc.pic_data_json or [])
            new_pic_no = f"2-{len(pics) + 1}"

            entry = {
                "pic_name": pic_name,
                "pic_path": saved_path,               # path เก็บไฟล์
                "pic_url": default_storage.url(saved_path),  # URL สำหรับแสดงผล
                "pic_no": new_pic_no,
            }
            pics.append(entry)
            doc.pic_data_json = pics
            doc.save(update_fields=["pic_data_json"])

            return JsonResponse({
                "status": "ok",
                "message": f"เพิ่มรูป '{pic_name}' (ภาพที่ {new_pic_no}) สำเร็จ",
                "picture": entry
            })

        # -------------------- 4) (ตัวอย่าง) สร้างเอกสาร .docx --------------------
        elif action == "generate_doc":
            # คุณสามารถ import เอนจิน docx บทที่ 2 มาต่อได้ในภายหลัง
            # จากโครงกลางใน doc_function ที่คุณใช้อยู่
            return HttpResponse("ยังไม่ได้เชื่อมเอนจิน .docx สำหรับบทที่ 2 (ตัวอย่าง action)")

        return JsonResponse({"status": "error", "message": f"ไม่รู้จัก action: {action}"})

    # -------------------- GET: แสดงหน้า template --------------------
    return render(request, "chapter_2.html", {
        "page_title": "บทที่ 2 เอกสาร/งานวิจัยที่เกี่ยวข้อง",
    })
