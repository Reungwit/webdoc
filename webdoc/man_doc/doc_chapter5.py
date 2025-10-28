# man_doc/doc_chapter5.py

from typing import List, Dict, Any, Iterable, Tuple

# 🔹 ใช้ยูทิลิตี้จากไฟล์กลาง (ไม่ต้องนิยามซ้ำ)
from man_doc.doc_function import (
    doc_setup,
    add_center_paragraph,
    add_left_paragraph,
    add_right_paragraph,
    add_paragraph_indent,
    add_wrapped_paragraph,
    add_page_break,
    apply_rest_page_margin,
)


# ========================= ค่ามาตรฐานตามคู่มือ (เฉพาะบทนี้) =========================
FONT_NAME = "TH SarabunPSK"
BASE_PT = 16
TITLE_PT = 20
LINE_LEN = 80           # ความยาวบรรทัดประมาณสำหรับตัดคำไทย

# ระยะกระดาษ
FIRST_TOP_INCH = 2.0        # หน้าแรก
REST_TOP_INCH  = 1.0        # หน้าถัดไป
LEFT_INCH  = 1.5
RIGHT_INCH = 1.0
BOTTOM_INCH = 1.0

# ระยะย่อบรรทัดแรก
FIRSTLINE_CM = 1.00
SUB_FIRSTLINE_CM = 1.50

# ========================= ตัวช่วยเพิ่มเติม (เฉพาะจัดระยะ) =========================
def apply_rest_page_margin(doc, top_inch: float = REST_TOP_INCH):
    """
    สร้าง section แบบ CONTINUOUS เพื่อเปลี่ยน top margin สำหรับหน้าถัดไป
    โดยไม่บังคับขึ้นหน้าใหม่
    """
    sec = doc.add_section(WD_SECTION.CONTINUOUS)
    sec.top_margin = Inches(top_inch)
    sec.bottom_margin = Inches(BOTTOM_INCH)
    sec.left_margin = Inches(LEFT_INCH)
    sec.right_margin = Inches(RIGHT_INCH)




# ========================= ฟังก์ชันหลัก (บทที่ 5) =========================
def doc_chapter5(intro_body: str, sections_json: List[Dict[str, Any]]):
    """
    สร้างบทที่ 5 ให้ตรงคู่มือ:
    - ฟอนต์ TH SarabunPSK ขนาด 16pt, บรรทัด 1.0 (ใช้ doc_setup เป็นฐาน)
    - หัวกลาง 2 บรรทัด (20pt หนา): 'บทที่ 5' และ 'สรุปผลการวิจัย อภิปรายผล และข้อเสนอแนะ'
    - ระยะกระดาษหน้าแรก: บน 2.0", ล่าง 1.0", ซ้าย 1.5", ขวา 1.0" (doc_setup ตั้งให้แล้ว)
      แล้วสลับเป็น top 1.0" สำหรับหน้าถัดไปด้วย section แบบต่อเนื่อง
    - ย่อหน้าเนื้อหา: ใช้ add_wrapped_paragraph (tap=1.0 ซม.) หรือ custom_tap
    """
    # ใช้ค่ามาตรฐานจากไฟล์กลาง
    doc = doc_setup()  # ตั้งฟอนต์/บรรทัด/มาร์จินหน้าแรกเป็นมาตรฐานเดียวกัน

    # ===== หัวเรื่องกลางหน้า =====
    add_center_paragraph(doc, "บทที่ 5", bold=True, font_size=TITLE_PT)
    add_center_paragraph(doc, "สรุปผลการวิจัย อภิปรายผล และข้อเสนอแนะ", bold=True, font_size=TITLE_PT)

    # เปลี่ยน top margin สำหรับหน้าถัดไปเป็น 1.0" (ไม่ขึ้นหน้าใหม่)
    apply_rest_page_margin(
        doc,
        top_inch=REST_TOP_INCH,
        left_inch=LEFT_INCH,
        right_inch=RIGHT_INCH,
        bottom_inch=BOTTOM_INCH
    )

    # ===== 5.1 บทนำ =====
    add_left_paragraph(doc, "5.1  บทนำ", bold=True)
    if (intro_body or "").strip():
        # ชิดซ้าย + ย่อบรรทัดแรก 1 ซม. + ตัดคำไทยรองรับ \t
        add_wrapped_paragraph(doc, intro_body, n=LINE_LEN, disth=True, tap=True)

    # ===== 5.2, 5.3, ... =====
    for i, (title, body, mains) in enumerate(iter_sections(sections_json), start=2):
        # หัวข้อใหญ่ (ตัวหนา)
        add_left_paragraph(doc, f"5.{i}  {title}".strip(), bold=True)

        # เนื้อหาหัวข้อใหญ่
        if body:
            add_wrapped_paragraph(doc, body, n=LINE_LEN, disth=True, tap=True)

        # หัวข้อหลัก 5.i.j
        for j, m in enumerate(mains or [], start=1):
            main_text = (m.get("text") or "").strip()
            if main_text:
                add_paragraph_indent(doc, f"5.{i}.{j}  {main_text}", bold=False, custom_tap=FIRSTLINE_CM)

            # หัวข้อย่อยข้อความ 5.i.j.k
            subs = m.get("subs") if isinstance(m.get("subs"), list) else []
            for k, s in enumerate(subs, start=1):
                s = (s or "").strip()
                if s:
                    add_wrapped_paragraph(
                        doc,
                        f"5.{i}.{j}.{k}  {s}",
                        n=LINE_LEN,
                        disth=True,
                        custom_tap=SUB_FIRSTLINE_CM
                    )

        # เว้นระยะเล็กน้อย
        doc.add_paragraph()

    return doc
