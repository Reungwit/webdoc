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

from backend.models import DocChapter1 as Chapter1

from man_doc.doc_chapter1 import doc_chapter1

DEFAULT_TITLES = [
    "ความเป็นมาและความสำคัญของปัญหา",
    "วัตถุประสงค์",
    "สมมุติฐาน",
    "ขอบเขตการทำโครงงาน",
    "ข้อตกลงเบื้องต้น",
    "นิยามศัพท์เฉพาะ",
    "ประโยชน์ที่คาดว่าจะได้รับ",
]

def _safe_parse_list(raw: Any, fallback: list) -> list:
    # รับได้ทั้ง str/list จากฟอร์มหรือ DB
    if isinstance(raw, list):
        return raw
    try:
        data = json.loads(raw or "[]")
        return data if isinstance(data, list) else (fallback or [])
    except Exception:
        return fallback or []

def _t(v: Any) -> str:
    return (v or "").strip() if isinstance(v, str) else ""

def _default_sections_for_ui() -> List[Dict[str, Any]]:
    # UI ต้องการหัวข้อแรกแบบ paragraphs, ที่เหลือใช้ body+points
    out: List[Dict[str, Any]] = []
    for i, t in enumerate(DEFAULT_TITLES):
        if i == 0:
            out.append({"title": t, "paragraphs": [], "points": []})
        else:
            out.append({"title": t, "body": "", "points": []})
    return out

# ---------- DB -> UI (แปลง mains -> points สำหรับหัวข้อ 1.2+) ----------
def _sections_ui_from_db(db_sections_any: Any) -> List[Dict[str, Any]]:
    db_sections = _safe_parse_list(db_sections_any, [])
    if not db_sections:
        return _default_sections_for_ui()

    ui = _default_sections_for_ui()
    for i, sec in enumerate(db_sections):
        if not isinstance(sec, dict):
            continue
        title = _t(sec.get("title") or sec.get("name") or sec.get("header") or (DEFAULT_TITLES[i] if i < len(DEFAULT_TITLES) else ""))

        # หัวข้อ 1.1 ใช้ paragraphs (แตกจาก body ได้ด้วย)
        if i == 0:
            paragraphs = []
            if isinstance(sec.get("paragraphs"), list) and sec["paragraphs"]:
                for it in sec["paragraphs"]:
                    s = _t(it if isinstance(it, str) else (it.get("text") if isinstance(it, dict) else ""))
                    if s: paragraphs.append(s)
            else:
                body = _t(sec.get("body"))
                if body:
                    paragraphs = [p.strip() for p in body.replace("\r\n", "\n").split("\n\n") if p.strip()]
            ui[0]["title"] = title
            ui[0]["paragraphs"] = paragraphs
            ui[0]["points"] = []  # ไม่ใช้ใน 1.1
            continue

        # หัวข้ออื่น ๆ
        ui[i]["title"] = title
        ui[i]["body"] = _t(sec.get("body"))
        # แปลง mains(list of {"text":..., "subs":[...]}) -> points(list of {"main":..., "subs":[...]})
        points = []
        mains = sec.get("mains") if isinstance(sec.get("mains"), list) else []
        for m in mains:
            if not isinstance(m, dict):
                continue
            main_text = _t(m.get("text") or m.get("title") or m.get("name"))
            subs_out = []
            subs = m.get("subs") if isinstance(m.get("subs"), list) else []
            for s in subs:
                subs_out.append(_t(s if isinstance(s, str) else (s.get("text") if isinstance(s, dict) else "")))
            points.append({"main": main_text, "subs": [x for x in subs_out if x]})
        ui[i]["points"] = points
    return ui

# ---------- UI -> DB (รองรับทั้ง points และ mains; เซฟเป็น mains) ----------
def _sections_db_from_ui(ui_any: Any) -> List[Dict[str, Any]]:
    ui = _safe_parse_list(ui_any, [])
    if not ui:
        return _default_sections_for_ui()

    out: List[Dict[str, Any]] = []
    for i, sec in enumerate(ui):
        if not isinstance(sec, dict):
            continue
        title = _t(sec.get("title") or (DEFAULT_TITLES[i] if i < len(DEFAULT_TITLES) else ""))

        if i == 0:
            # 1.1 ใช้ paragraphs + ทำ body = join ไว้เผื่อระบบเก่า
            paras = []
            paras_in = sec.get("paragraphs")
            if isinstance(paras_in, list):
                for it in paras_in:
                    s = _t(it if isinstance(it, str) else (it.get("text") if isinstance(it, dict) else ""))
                    if s: paras.append(s)
            body = "\n\n".join(paras)
            out.append({"title": title, "paragraphs": paras, "body": body, "mains": []})
            continue

        body = _t(sec.get("body"))

        # รับ points หรือ mains ก็ได้ แล้ว normalize เป็น mains
        mains_out = []
        if isinstance(sec.get("mains"), list) and sec["mains"]:
            for m in sec["mains"]:
                if not isinstance(m, dict): continue
                text = _t(m.get("text") or m.get("title") or m.get("name"))
                subs_in = m.get("subs") if isinstance(m.get("subs"), list) else []
                subs = []
                for s in subs_in:
                    subs.append(_t(s if isinstance(s, str) else (s.get("text") if isinstance(s, dict) else "")))
                mains_out.append({"text": text, "subs": [x for x in subs if x]})
        elif isinstance(sec.get("points"), list):
            for p in sec["points"]:
                if isinstance(p, dict):
                    text = _t(p.get("main") or p.get("text") or p.get("title"))
                    subs_in = p.get("subs") if isinstance(p.get("subs"), list) else []
                    subs = []
                    for s in subs_in:
                        subs.append(_t(s if isinstance(s, str) else (s.get("text") if isinstance(s, dict) else "")))
                    mains_out.append({"text": text, "subs": [x for x in subs if x]})
                elif isinstance(p, str):
                    txt = _t(p)
                    if txt: mains_out.append({"text": txt, "subs": []})

        out.append({"title": title, "body": body, "mains": mains_out})
    return out

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
                sections_db = _sections_db_from_ui(ui_in)

                # รองรับ JSONField / TextField
                defaults = {"intro_body": intro_body, "updated_at": timezone.now()}
                try:
                    defaults["sections_json"] = sections_db
                    Chapter1.objects.update_or_create(user_id=user_pk, defaults=defaults)
                except Exception:
                    Chapter1.objects.update_or_create(user_id=user_pk, defaults=defaults)
                    # บันทึกเป็น string ถ้าเป็น TextField
                    Chapter1.objects.filter(user_id=user_pk).update(
                        sections_json=json.dumps(sections_db, ensure_ascii=False)
                    )

                # โหลดกลับมาแสดง
                row = Chapter1.objects.filter(user_id=user_pk).order_by("-updated_at").first()
                db_intro = (getattr(row, "intro_body", "") or "")
                db_sections = _safe_parse_list(getattr(row, "sections_json", []), [])
                ui_sections = _sections_ui_from_db(db_sections)

                messages.success(request, "💾 บันทึกข้อมูลบทที่ 1 เรียบร้อยแล้ว")
                return render(request, "chapter_1.html", {
                    "initial": {"intro_body": db_intro, "chapter1_json": ui_sections}
                })

            elif action == "get_data":
                ui_sections = _sections_ui_from_db(db_sections)
                messages.info(request, "🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว")
                return render(request, "chapter_1.html", {
                    "initial": {"intro_body": db_intro, "chapter1_json": ui_sections}
                })

            elif action == "generate_docx":
                ui_in = _safe_parse_list(raw_json, [])
                sections_for_doc = _sections_db_from_ui(ui_in) if ui_in else db_sections
                if not intro_body:
                    intro_body = db_intro

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
        ui_sections = _sections_ui_from_db(db_sections)
        return render(request, "chapter_1.html", {
            "initial": {"intro_body": db_intro, "chapter1_json": ui_sections}
        })

    # GET
    ui_sections = _sections_ui_from_db(db_sections)
    return render(request, "chapter_1.html", {
        "initial": {
            "intro_body": (db_intro if (db_intro or db_sections) else ""),
            "chapter1_json": ui_sections,
        }
    })
