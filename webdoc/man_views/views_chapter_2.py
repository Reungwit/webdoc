from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json

# -------------------------------------------------------------
# โครงข้อมูล (phase: mock) — ยังไม่แตะฐานข้อมูลจริง
# -------------------------------------------------------------
DEFAULT_SECTIONS = [
    {
        "title_no": "2.1",
        "title": "แนวคิดและทฤษฎีที่เกี่ยวข้อง",
        # ย่อหน้าใหญ่ของหัวข้อ (หลายย่อหน้าได้)
        "body_paragraphs": [],
        # โครงย่อยแบบ tree: items = [{text, paragraphs:[], children:[...]}]
        "items": [],
        "pictures": []  # [{pic_no, pic_name, pic_path}]
    },
    {
        "title_no": "2.2",
        "title": "งานวิจัยที่เกี่ยวข้อง",
        "body_paragraphs": [],
        "items": [],
        "pictures": []
    }
]

def _safe_json_loads(s, default):
    try:
        return json.loads(s)
    except Exception:
        return default

@login_required
def chapter_2_view(request):
    """
    บทที่ 2 (phase: mock)
    - หน้าเว็บทำงานครบ, เพิ่มหัวข้อย่อยได้หลายระดับ, แนบรูปต่อหัวข้อใหญ่
    - ยังไม่เชื่อมฐานข้อมูลจริง / ยังไม่ generate docx จริง
    """
    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()

        # ----------------- 1) GET DATA -----------------
        if action == "get_data":
            # ส่งค่าเริ่มต้น (mock) เป็นสองหัวข้อคงที่
            initial = {
                "intro_body": "",
                "sections": DEFAULT_SECTIONS
            }
            return JsonResponse({
                "status": "ok",
                "initial": initial
            })

        # ----------------- 2) SAVE -----------------
        elif action == "save":
            intro_body = request.POST.get("intro_body", "")
            sections_raw = request.POST.get("sections_json", "[]")
            sections_data = _safe_json_loads(sections_raw, [])

            # phase mock: แค่ echo กลับเพื่อยืนยันโครง
            return JsonResponse({
                "status": "ok",
                "message": "บันทึก (mock) เรียบร้อย",
                "echo": {
                    "intro_body": intro_body,
                    "sections": sections_data
                }
            })

        # ----------------- 3) ADD PICTURE (ต่อหัวข้อใหญ่) -----------------
        elif action == "add_picture":
            # ระบุหัวข้อใหญ่ที่จะแนบรูป เช่น "2.1" หรือ "2.2"
            section_no = (request.POST.get("section_no") or "").strip()
            pic_name   = (request.POST.get("pic_name") or "").strip()
            # ใน phase mock จะไม่ได้อัปโหลดจริง แต่รองรับไฟล์เข้ามาแล้ว
            _pic_file  = request.FILES.get("pic_file")  # noqa

            if not section_no:
                return JsonResponse({"status": "error", "message": "ไม่พบเลขหัวข้อ section_no"})
            if section_no not in ("2.1", "2.2"):
                return JsonResponse({"status": "error", "message": "section_no ต้องเป็น 2.1 หรือ 2.2"})
            if not pic_name:
                return JsonResponse({"status": "error", "message": "กรุณากรอกชื่อรูป"})

            # mock running number (เช่น ภาพที่ 2-1, 2-2 ... — ที่จริงควรอ่านจาก DB)
            # ในที่นี้ให้ fix เป็น 2-99 เพื่อยืนยัน flow
            fake_no = "2-99"
            # path mock (ถ้ามีไฟล์จะใช้ชื่อไฟล์; ถ้าไม่มีก็ว่าง)
            fake_path = _pic_file.name if _pic_file else (request.POST.get("pic_path") or "")

            return JsonResponse({
                "status": "ok",
                "message": f"เพิ่มรูป (mock) แล้วในหัวข้อ {section_no} : {fake_no}",
                "picture": {
                    "pic_no": fake_no,
                    "pic_name": pic_name,
                    "pic_path": fake_path
                },
                "section_no": section_no
            })

        # ----------------- 4) GENERATE DOC (mock) -----------------
        elif action == "generate_doc":
            return HttpResponse("กำลังอยู่ในโหมด mock: ยังไม่ generate .docx", content_type="text/plain")

        # ----------------- unknown action -----------------
        return JsonResponse({"status": "error", "message": f"ไม่รู้จัก action: {action}"})

    # GET: render หน้า
    return render(request, "chapter_2.html", {
        "page_title": "บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง"
    })