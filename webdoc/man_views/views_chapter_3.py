# man_views/views_chapter_3.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db import transaction
import json
import logging

from backend.models import DocChapter3

logger = logging.getLogger(__name__)


# ---------- Utils ----------
def _to_list_or_fallback(value, fallback=None):
    """
    แปลงข้อมูลให้เป็น list อย่างปลอดภัย:
      - ถ้าเป็น list อยู่แล้ว → คืนค่าเดิม
      - ถ้าเป็น str → พยายาม json.loads ถ้าไม่สำเร็จ → fallback หรือ []
      - อื่น ๆ / None → fallback หรือ []
    """
    try:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            s = value.strip()
            if s == "":
                return (fallback or [])
            parsed = json.loads(s)
            return parsed if isinstance(parsed, list) else (fallback or [])
        return (fallback or [])
    except (json.JSONDecodeError, TypeError, ValueError):
        return (fallback or [])


def _extract_list_from_request(request, key_candidates, fallback=None):
    """
    ดึง list จาก request โดยลองหลายชื่อคีย์ (key_candidates)
    รองรับ:
      1) form-encoded แบบหลายค่า: key[]  → request.POST.getlist(...)
      2) form-encoded แบบสตริง JSON: key → request.POST.get(...)
      3) application/json body: {key: [...]} หรือ {key: "[]"}
    ถ้าไม่เจอเลย → คืน fallback
    """
    # 1) ลอง key[] ใน form ก่อน (เช่น chapter3_tables_json[])
    for base in key_candidates:
        many_key = f"{base}[]"
        many_vals = request.POST.getlist(many_key)
        if many_vals:
            normalized = []
            for item in many_vals:
                try:
                    # แต่ละรายการอาจถูกส่งเป็น JSON string
                    normalized.append(json.loads(item))
                except Exception:
                    normalized.append(item)
            return normalized

    # 2) ลอง key (สตริง JSON)
    for base in key_candidates:
        raw = request.POST.get(base, None)
        if raw is not None:
            return _to_list_or_fallback(raw, fallback=fallback)

    # 3) ลองอ่านจาก JSON body
    ctype = (request.META.get("CONTENT_TYPE") or "").lower()
    if "application/json" in ctype:
        try:
            body = json.loads(request.body.decode("utf-8") or "{}")
            for base in key_candidates:
                if base in body:
                    return _to_list_or_fallback(body.get(base), fallback=fallback)
                # กันเผื่อ key[] ใน body (พบน้อยมาก)
                arr_key = f"{base}[]"
                if arr_key in body:
                    return _to_list_or_fallback(body.get(arr_key), fallback=fallback)
        except Exception:
            pass

    # ไม่พบสักคีย์ → คืน fallback
    return (fallback or [])


def _extract_string_from_request(request, key, default=""):
    """
    ดึงค่าสตริงจาก form หรือ JSON body
    """
    val = request.POST.get(key)
    if val is not None:
        return (val or "").strip()
    ctype = (request.META.get("CONTENT_TYPE") or "").lower()
    if "application/json" in ctype:
        try:
            body = json.loads(request.body.decode("utf-8") or "{}")
            return (body.get(key) or "").strip()
        except Exception:
            return default
    return default


# ---------- View ----------
@login_required
@require_http_methods(["GET", "POST"])
def chapter_3_view(request):
    """
    จัดการบทที่ 3:
      - GET  : โหลดค่าล่าสุดของผู้ใช้
      - POST : action=save     → บันทึก intro_body, sections_json, tb_sections_json
               action=get_data → คืนค่าล่าสุด
    """
    user = request.user

    # โหลดเรคคอร์ดล่าสุดของผู้ใช้ (ถ้ายังไม่มีจะเป็น None)
    row = DocChapter3.objects.filter(user=user).order_by("-updated_at").first()

    # ค่า default จาก DB (กัน None และชนิดไม่ตรง)
    db_intro = (row.intro_body if row else "") or ""
    db_secs = row.sections_json if (row and isinstance(row.sections_json, list)) else []
    db_tables = row.tb_sections_json if (row and isinstance(row.tb_sections_json, list)) else []

    if request.method == "GET":
        return render(request, "chapter_3.html", {
            "initial": {
                "intro_body": db_intro,
                "chapter3_json": db_secs,
                "chapter3_tables_json": db_tables,
            }
        })

    # ---------- POST ----------
    action = (request.POST.get("action") or "").strip()
    if not action:
        # กันกรณีส่ง JSON body
        action = _extract_string_from_request(request, "action", default="")

    # intro_body
    intro_body = _extract_string_from_request(request, "intro_body", default=db_intro)

    # sections (ตัวเนื้อหา)
    sections_key_candidates = [
        "chapter3_json",
        "sections_json",     # กันชื่อย่อ/ชื่อคอลัมน์
        "sections"           # กันบางฟร้อนท์
    ]
    secs_in = _extract_list_from_request(request, sections_key_candidates, fallback=db_secs)
    if not isinstance(secs_in, list):
        secs_in = db_secs

    # tables (ประเด็นหลักที่ “ไม่ยอมบันทึก”)
    # รองรับ alias ชื่อคีย์หลายแบบ
    tables_key_candidates = [
        "chapter3_tables_json",
        "chapter3_table_json",
        "tb_sections_json",
        "tb_sections",
        "tables_json",
        "tables"
    ]
    tables_in = _extract_list_from_request(request, tables_key_candidates, fallback=db_tables)

    # ทำความสะอาดค่าตารางเบื้องต้น (ตัด None/ค่าว่าง)
    if isinstance(tables_in, list):
        tables_in = [t for t in tables_in if t not in (None, "", {})]
    else:
        tables_in = db_tables

    if action == "get_data":
        messages.info(request, "🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว")
        return render(request, "chapter_3.html", {
            "initial": {
                "intro_body": db_intro,
                "chapter3_json": db_secs,
                "chapter3_tables_json": db_tables,
            }
        })

    if action != "save":
        messages.info(request, "ยังไม่รองรับการทำงานนี้")
        return render(request, "chapter_3.html", {
            "initial": {
                "intro_body": db_intro,
                "chapter3_json": db_secs,
                "chapter3_tables_json": db_tables,
            }
        })

    # ---------- SAVE ----------
    try:
        with transaction.atomic():
            DocChapter3.objects.update_or_create(
                user=user,
                defaults={
                    "intro_body": intro_body,
                    "sections_json": secs_in,        # JSONField ← Python list
                    "tb_sections_json": tables_in,   # JSONField ← Python list (สำคัญ)
                    "chap_id": 3,
                    "updated_at": timezone.now(),
                }
            )
    except Exception as e:
        # ล็อกแล้วแจ้งผู้ใช้แบบอ่านง่าย
        logger.exception("Save Chapter 3 failed")
        messages.error(request, f"❌ บันทึกไม่สำเร็จ: {e}")
        # คืนค่าเดิมจาก DB
        return render(request, "chapter_3.html", {
            "initial": {
                "intro_body": db_intro,
                "chapter3_json": db_secs,
                "chapter3_tables_json": db_tables,
            }
        })

    # โหลดกลับมาโชว์ (กันค่าเก่า/cache)
    row = DocChapter3.objects.filter(user=user).order_by("-updated_at").first()
    out_intro = (row.intro_body if row else "") or ""
    out_secs = row.sections_json if (row and isinstance(row.sections_json, list)) else []
    out_tables = row.tb_sections_json if (row and isinstance(row.tb_sections_json, list)) else []

    messages.success(request, "💾 บันทึกข้อมูลบทที่ 3 เรียบร้อยแล้ว")
    return render(request, "chapter_3.html", {
        "initial": {
            "intro_body": out_intro,
            "chapter3_json": out_secs,
            "chapter3_tables_json": out_tables,
        }
    })
