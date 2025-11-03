from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json, re

def _empty_node():
    return {"text": "", "paragraphs": [], "children": [], "pictures": []}

DEFAULT_SECTIONS = [
    {
        "title_no": "2.1",
        "title": "แนวคิดและทฤษฎีที่เกี่ยวข้อง",
        "body_paragraphs": [],
        "items": [_empty_node()],   # เริ่มต้นมี 2.1.1
    },
    {
        "title_no": "2.2",
        "title": "งานวิจัยที่เกี่ยวข้อง",
        "body_paragraphs": [],
        "items": [_empty_node()],   # เริ่มต้นมี 2.2.1 (จะไม่มีกล่องรูป)
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
    phase: mock
    - กล่องรูปจะแสดงในทุกหัวข้อย่อยระดับแรกของ 2.1 (2.1.x ทั้งหมด)
    - ยังไม่เชื่อม DB / ยังไม่ generate docx
    """
    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()

        if action == "get_data":
            return JsonResponse({"status": "ok", "initial": {
                "intro_body": "",
                "sections": DEFAULT_SECTIONS
            }})

        elif action == "save":
            intro_body = request.POST.get("intro_body", "")
            sections_raw = request.POST.get("sections_json", "[]")
            sections_data = _safe_json_loads(sections_raw, [])
            return JsonResponse({"status": "ok", "message": "บันทึก (mock) เรียบร้อย", "echo": {
                "intro_body": intro_body,
                "sections": sections_data
            }})

        elif action == "add_picture_node":
            section_no = (request.POST.get("section_no") or "").strip()   # ต้องเป็น "2.1"
            node_no    = (request.POST.get("node_no") or "").strip()      # เช่น "2.1.3"
            pic_name   = (request.POST.get("pic_name") or "").strip()
            f          = request.FILES.get("pic_file")

            if not section_no or not node_no:
                return JsonResponse({"status": "error", "message": "ข้อมูลไม่ครบ section_no/node_no"})
            if section_no != "2.1" or not re.fullmatch(r"2\.1\.\d+", node_no):
                return JsonResponse({"status": "error", "message": "อนุญาตเฉพาะหัวข้อย่อยระดับแรกของ 2.1 (2.1.x) เท่านั้น"})
            if not pic_name:
                return JsonResponse({"status": "error", "message": "กรุณากรอกชื่อรูป"})

            fake_no = "2-99"
            fake_path = f.name if f else (request.POST.get("pic_path") or "")
            return JsonResponse({
                "status": "ok",
                "message": f"เพิ่มรูป (mock) แล้วในหัวข้อ {node_no} : {fake_no}",
                "picture": {"pic_no": fake_no, "pic_name": pic_name, "pic_path": fake_path},
                "section_no": section_no, "node_no": node_no
            })

        elif action == "generate_doc":
            return HttpResponse("กำลังอยู่ในโหมด mock: ยังไม่ generate .docx", content_type="text/plain")

        return JsonResponse({"status": "error", "message": f"ไม่รู้จัก action: {action}"})

    return render(request, "chapter_2.html", {"page_title": "บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง"})
