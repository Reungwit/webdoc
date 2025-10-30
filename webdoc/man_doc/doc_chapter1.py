# man_doc/doc_chapter1.py
from typing import List, Dict, Any
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.section import WD_SECTION

from man_doc.doc_function import (
    doc_setup,
    add_center_paragraph,
    add_left_paragraph,
    add_paragraph_indent,
    add_wrapped_paragraph,
)

TITLE_PT = 20
LINE_LEN = 85                 # ความยาวบรรทัดโดยประมาณสำหรับตัดคำไทย
FIRSTLINE_CM = 1.00           # ระยะย่อบรรทัดแรกของ "ย่อหน้าใหญ่"
SUB_FIRSTLINE_CM = 1.50       # ระยะย่อของหัวข้อย่อย

def apply_rest_page_margin(doc: Document, top_inch: float = 1.0):
    """ปรับ top margin ของหน้าถัดไป (ต่อเนื่อง ไม่ขึ้นหน้าใหม่)"""
    sec = doc.add_section(WD_SECTION.CONTINUOUS)
    base = doc.sections[0]
    sec.top_margin = Inches(top_inch)
    sec.bottom_margin = base.bottom_margin
    sec.left_margin = base.left_margin
    sec.right_margin = base.right_margin

def _text(v: Any) -> str:
    return (v or "").strip() if isinstance(v, str) else ""

def _coerce_paragraph_list(sec: Dict[str, Any]) -> List[str]:
    """
    คืนลิสต์ของ 'ย่อหน้าใหญ่' สำหรับหัวข้อ 1.1
    รองรับทั้ง
      - body: "ข้อความ\n\nข้อความ..." (จะแตกตามบรรทัดว่าง)
      - paragraphs / paras: ["ย่อหน้า 1", "ย่อหน้า 2", ...]
    """
    # 1) ถ้าให้มาเป็นลิสต์โดยตรง
    for key in ("paragraphs", "paras"):
        vals = sec.get(key)
        if isinstance(vals, list):
            out = []
            for x in vals:
                s = _text(x if isinstance(x, str) else (x.get("text") if isinstance(x, dict) else ""))
                if s:
                    out.append(s)
            if out:
                return out

    # 2) ถ้าให้มาเป็นสตริงยาวใน body → แตกด้วยบรรทัดว่าง
    body = _text(sec.get("body"))
    if not body:
        return []
    # แยกด้วยเว้นบรรทัด (1+ บรรทัดว่าง)
    parts = [p.strip() for p in body.replace("\r\n", "\n").split("\n\n") if p.strip()]
    return parts

def doc_chapter1(intro_body: str, sections_json: List[Dict[str, Any]]) -> Document:
    """
    จัดเลขหัวข้อให้ตรงกับ UI:
      - บทนำ (ไม่ใส่เลข)
      - 1.1, 1.2, ... / 1.x.y / 1.x.y.z
    หมายเหตุ: หัวข้อ 1.1 รองรับ 'ย่อหน้าใหญ่หลายย่อหน้า' และย่อบรรทัดแรกให้โดยอัตโนมัติ
    """
    # ตั้งค่าหน้าเอกสารพื้นฐาน
    doc = doc_setup()

    # หัวเรื่องกลางหน้า
    add_center_paragraph(doc, "บทที่ 1", bold=True, font_size=TITLE_PT)
    add_center_paragraph(doc, "บทนำ", bold=True, font_size=TITLE_PT)

    # ปรับ margin หน้าถัดไป
    apply_rest_page_margin(doc, top_inch=1.0)

    # ----- บทนำ (ไม่ใส่เลข) -----
    add_left_paragraph(doc, "", bold=True)
    if _text(intro_body):
        # ย่อบรรทัดแรกของบทนำเหมือนกัน (ถ้าต้องการไม่ย่อ ให้เอา custom_tap ออก)
        add_wrapped_paragraph(doc, _text(intro_body), n=LINE_LEN, disth=True, custom_tap=FIRSTLINE_CM)
    doc.add_paragraph()

    # ----- หัวข้อใหญ่ 1.1, 1.2, ... -----
    sections = sections_json if isinstance(sections_json, list) else []
    for i, sec in enumerate(sections, start=1):
        title = _text(sec.get("title"))
        add_left_paragraph(doc, f"1.{i}  {title}".strip(), bold=True)

        # --- เนื้อหา/ย่อหน้าใหญ่ ---
        if i == 1:
            # เฉพาะหัวข้อ 1.1: รองรับหลายย่อหน้าใหญ่และย่อบรรทัดแรกอัตโนมัติ
            paras = _coerce_paragraph_list(sec)
            for para in paras:
                add_wrapped_paragraph(
                    doc,
                    para,
                    n=LINE_LEN,
                    disth=True,
                    custom_tap=FIRSTLINE_CM,   # ← ย่อบรรทัดแรก
                )
        else:
            # หัวข้ออื่น ๆ แสดง body ธรรมดา 1 บล็อค (ถ้าต้องการให้หลายย่อหน้าเหมือน 1.1 ให้ใช้ _coerce_paragraph_list เหมือนกัน)
            body = _text(sec.get("body"))
            if body:
                add_wrapped_paragraph(doc, body, n=LINE_LEN, disth=True, tap=True)

        # --- หัวข้อหลัก (1.x.y) และย่อย (1.x.y.z) ---
        mains = sec.get("mains") if isinstance(sec.get("mains"), list) else []
        for j, m in enumerate(mains, start=1):
            main_text = _text(m.get("text"))
            if main_text:
                add_paragraph_indent(doc, f"1.{i}.{j}  {main_text}", bold=False, custom_tap=FIRSTLINE_CM)

            subs = m.get("subs") if isinstance(m.get("subs"), list) else []
            for k, s in enumerate(subs, start=1):
                sub_text = _text(s if isinstance(s, str) else (s.get("text") if isinstance(s, dict) else ""))
                if sub_text:
                    add_wrapped_paragraph(
                        doc,
                        f"1.{i}.{j}.{k}  {sub_text}",
                        n=LINE_LEN,
                        disth=True,
                        custom_tap=SUB_FIRSTLINE_CM,
                    )
        doc.add_paragraph()

    return doc
