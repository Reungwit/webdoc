# man_doc/doc_chapter5.py
from typing import List, Dict, Any
from docx.shared import Pt, Cm, Inches
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn

from man_doc.doc_function import (
    doc_setup,
    add_center_paragraph,
    add_left_paragraph,
    add_paragraph_indent,
    add_wrapped_paragraph,
    iter_sections,
)

# ========================= ค่ามาตรฐานตามคู่มือ =========================
TITLE_PT = 20
LINE_LEN = 80
FIRSTLINE_CM = 1.00
SUB_FIRSTLINE_CM = 1.50

# ========================= ตัวช่วยเพิ่มเติม (เฉพาะจัดระยะ) =========================
def apply_rest_page_margin(doc, top_inch: float = 1.0):
    """
    เปลี่ยน top margin สำหรับหน้าถัดไปเป็น top_inch โดยไม่ขึ้นหน้าใหม่
    """
    sec = doc.add_section(WD_SECTION.CONTINUOUS)
    sec.top_margin = Inches(top_inch)
    # ถ้าต้องการคงค่า margin อื่นให้เท่ากับหน้าแรก ให้คัดลอกจาก section[0] ก็ได้
    base = doc.sections[0]
    sec.bottom_margin = base.bottom_margin
    sec.left_margin   = base.left_margin
    sec.right_margin  = base.right_margin

# ========================= ฟังก์ชันหลัก =========================
def doc_chapter5(intro_body: str, sections_json: List[Dict[str, Any]]):
    """
    สร้างบทที่ 5 โดยใช้ doc_setup() สำหรับตั้งค่าหน้าแรก และปรับหน้าถัดไปด้วย apply_rest_page_margin
    """
    # ✅ ใช้หน้าแรก/ฟอนต์/บรรทัด จาก doc_setup()
    doc = doc_setup()

    # ===== หัวเรื่องกลางหน้า =====
    add_center_paragraph(doc, "บทที่ 5", bold=True, font_size=TITLE_PT)
    add_center_paragraph(doc, "สรุปผลการวิจัย อภิปรายผล และข้อเสนอแนะ", bold=True, font_size=TITLE_PT)

    # ✅ ปรับ margin หน้าถัดไปเป็น 1.0" แบบไม่ขึ้นหน้าใหม่
    apply_rest_page_margin(doc, top_inch=1.0)

    # ===== 5.1 บทนำ =====
    add_left_paragraph(doc, "5.1  บทนำ", bold=True)
    if (intro_body or "").strip():
        add_wrapped_paragraph(doc, intro_body, n=LINE_LEN, disth=True, tap=True)

    # ===== 5.2, 5.3, ... =====
    for i, (title, body, mains) in enumerate(iter_sections(sections_json), start=2):
        add_left_paragraph(doc, f"5.{i}  {title}".strip(), bold=True)

        if body:
            add_wrapped_paragraph(doc, body, n=LINE_LEN, disth=True, tap=True)

        for j, m in enumerate(mains or [], start=1):
            main_text = (m.get("text") or "").strip()
            if main_text:
                add_paragraph_indent(doc, f"5.{i}.{j}  {main_text}", bold=False, custom_tap=FIRSTLINE_CM)

            subs = m.get("subs") if isinstance(m.get("subs"), list) else []
            for k, s in enumerate(subs, start=1):
                s = (s or "").strip()
                if s:
                    add_wrapped_paragraph(
                        doc,
                        f"5.{i}.{j}.{k}  {s}",
                        n=LINE_LEN,
                        disth=True,
                        custom_tap=SUB_FIRSTLINE_CM,
                    )

        doc.add_paragraph()

    return doc
