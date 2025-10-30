# man_views/views_chapter_1.py
from __future__ import annotations
import json
from io import BytesIO
from typing import Any, List, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

try:
    from backend.models import DocChapter1 as Chapter1
except Exception:
    from backend.models import SpChapter1 as Chapter1

from man_doc.doc_chapter1 import doc_chapter1

from man_doc.doc_function import (
    _safe_parse_list,
    sections_db_from_ui,
    sections_ui_from_db,
    sections_doc_safe,
)

DEFAULT_TITLES = [
    "ความเป็นมาและความสำคัญของปัญหา",
    "วัตถุประสงค์",
    "สมมุติฐาน",
    "ขอบเขตการทำโครงงาน",
    "ข้อตกลงเบื้องต้น",
    "นิยามศัพท์เฉพาะ",
    "ประโยชน์ที่คาดว่าจะได้รับ",
]
FIRST_MODE = "paragraphs"


@login_required
def chapter_1_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_pk = getattr(user, "user_id", None) or getattr(user, "id", None)

    row = Chapter1.objects.filter(user_id=user_pk).order_by("-updated_at").first()

    db_intro = (getattr(row, "intro_body", "") or "")
    # sections_json อาจเป็น list หรือ str
    db_sections_raw = getattr(row, "sections_json", [])
    db_sections = _safe_parse_list(db_sections_raw, [])

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        intro_body = (request.POST.get("intro_body") or "").strip()
        raw_json = request.POST.get("chapter1_json", "")

        try:
            if action == "save":
                ui_in = _safe_parse_list(raw_json, [])
                sections_db = sections_db_from_ui(
                    ui_in,
                    default_titles=DEFAULT_TITLES,
                    first_section_mode=FIRST_MODE,
                )

            elif action == "get_data":
                ui_sections = sections_ui_from_db(
                db_sections,
                default_titles=DEFAULT_TITLES,
                first_section_mode=FIRST_MODE,
                )

            elif action == "generate_docx":
                ui_in = _safe_parse_list(raw_json, [])
                sections_for_doc = (
                    sections_db_from_ui(ui_in, default_titles=DEFAULT_TITLES, first_section_mode=FIRST_MODE)
                    if ui_in else db_sections
                )
                sections_for_doc = sections_doc_safe(
                    sections_for_doc,
                    default_titles=DEFAULT_TITLES,
                    first_section_mode=FIRST_MODE,
                )

                doc = doc_chapter1(intro_body, sections_for_doc)
                buf = BytesIO()
                doc.save(buf)
                buf.seek(0)
                return FileResponse(
                    buf,
                    as_attachment=True,
                    filename="chapter1.docx",
                    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            else:
                messages.info(request, "ยังไม่รองรับการทำงานนี้")

        except Exception as e:
            messages.error(request, f"เกิดข้อผิดพลาด: {type(e).__name__}: {e}")

        # fallback: แสดงข้อมูลล่าสุดแทนหน้าว่าง
        ui_sections = sections_ui_from_db(db_sections)
        return render(request, "chapter_1.html", {
            "initial": {"intro_body": db_intro, "chapter1_json": ui_sections}
        })

    # GET
    ui_sections = sections_ui_from_db(db_sections)
    return render(request, "chapter_1.html", {
        "initial": {
            "intro_body": (db_intro if (db_intro or db_sections) else ""),
            "chapter1_json": ui_sections,
        }
    })
