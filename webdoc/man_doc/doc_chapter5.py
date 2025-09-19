# man_doc/doc_chapter5.py
# -*- coding: utf-8 -*-
from typing import List, Dict, Any, Iterable, Tuple
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pythainlp.tokenize import word_tokenize
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from docx.document import Document as DocxDocument

# ========================= ค่ามาตรฐานตามคู่มือ =========================
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


# ========================= ฟังก์ชันตามที่ผู้ใช้กำหนด =========================
def add_center_paragraph(doc, text, bold=False ,font_size=16):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        p.runs[0].bold = False
    if p.runs:
        p.runs[0].font.size = Pt(font_size)  # ตั้งค่าขนาดฟอนต์ในพารากราฟ
    return p

def add_left_paragraph(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        p.runs[0].bold = False
    return p

def add_right_paragraph(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        p.runs[0].bold = False
    return p

def add_paragraph_indent(doc, text, bold=False, custom_tap: float = 0.0):
    p = doc.add_paragraph(text)
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        p.runs[0].bold = False

    if custom_tap:
        p.paragraph_format.first_line_indent = Cm(custom_tap)
    else:
        p.paragraph_format.first_line_indent = Cm(1.00)
    return p

def add_wrapped_paragraph(p_or_doc, text: str, n: int, disth: bool = False ,extap: bool = False,tap: bool = False , custom_tap: float = 0.0):
    """
    สร้างหรือเพิ่มข้อความที่ถูกตัดคำลงใน paragraph หรือ document/cell
    disth=True จะใช้ thaiDistribute แทน justify
    """

    def set_thai_distributed(paragraph):
        p_pr = paragraph._p.get_or_add_pPr()
        jc = OxmlElement('w:jc')
        jc.set(qn('w:val'), 'thaiDistribute')
        p_pr.append(jc)

    # ตัดคำแบบภาษาไทย
    # words = word_tokenize(text, engine="newmm")
    # แบ่งบรรทัดตามความยาว n
    
    lines = []
    for paragraph in text.split("\n"):
        words = word_tokenize(paragraph.strip(), engine="newmm")
        line = ""
        for word in words:
            if len(line + word) <= n:
                line += word + ""
            else:
                lines.append(line.strip())
                line = word + ""
        if line:
            lines.append(line.strip())

    # # ตรวจสอบว่าเป็น doc/cell หรือ paragraph
    if isinstance(p_or_doc, (DocxDocument, _Cell)):
        p = p_or_doc.add_paragraph()
    elif isinstance(p_or_doc, Paragraph):
        p = p_or_doc
    else:
        raise TypeError("Argument must be Document, _Cell, or Paragraph")

    # เพิ่มข้อความ
    for idx, l in enumerate(lines):
        tab_count = len(l) - len(l.lstrip("\t"))  # นับจำนวน \t ต้นบรรทัด
        l = l.lstrip("\t")  # ลบ \t ทิ้ง เพื่อใส่ข้อความจริง

    #  ✅ ใส่ tab ตามจำนวน
        for _ in range(tab_count):
            p.add_run().add_tab()

    # ✅ ใส่ข้อความที่เหลือ (ถ้าเหลือ)
        if l.strip():  # ป้องกันบรรทัดว่าง
            p.add_run(l)

        if idx < len(lines) - 1:
            p.add_run().add_break()

    # ตั้งค่าการจัดรูปแบบ paragraph
    
    p.paragraph_format.keep_together = True
    p.paragraph_format.keep_with_next = True

    
    if disth:
        set_thai_distributed(p)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
         
         # ตั้งค่าการจัดรูปแบบ paragraph
    if extap :
        p.paragraph_format.first_line_indent = Cm(1.80)
    elif tap :
        p.paragraph_format.first_line_indent = Cm(1.00)
    elif custom_tap:
        p.paragraph_format.first_line_indent = Cm(custom_tap)

        
    return p

def add_page_break(doc, top_margin_inch=1.5):
    """
    แทรก Page Break แล้วกำหนดขอบกระดาษด้านบนของหน้าถัดไป
    เรียกใช้ add_page_break(doc)
    """
    new_section = doc.add_section(WD_SECTION.NEW_PAGE)
    new_section.top_margin = Inches(top_margin_inch)


# ========================= ตัวช่วยเพิ่มเติม (เฉพาะจัดระยะ) =========================
def _apply_rest_page_margin(doc, top_inch: float = REST_TOP_INCH):
    """
    สร้าง section แบบ CONTINUOUS เพื่อเปลี่ยน top margin สำหรับหน้าถัดไป
    โดยไม่บังคับขึ้นหน้าใหม่
    """
    sec = doc.add_section(WD_SECTION.CONTINUOUS)
    sec.top_margin = Inches(top_inch)
    sec.bottom_margin = Inches(BOTTOM_INCH)
    sec.left_margin = Inches(LEFT_INCH)
    sec.right_margin = Inches(RIGHT_INCH)


# ========================= ตัวช่วยอ่านข้อมูลจาก UI =========================
def _iter_sections(sections: List[Dict[str, Any]]) -> Iterable[Tuple[str, str, List[Dict[str, Any]]]]:
    """
    รองรับ schema จากหน้า chapter_5.html
      [{ title, body, points:[{ main, subs:[str] }] }, ...]
    """
    sections = sections if isinstance(sections, list) else []
    for sec in sections:
        if not isinstance(sec, dict):
            continue
        title = (sec.get("title") or sec.get("header") or sec.get("name") or "").strip()
        body  = (sec.get("body")  or sec.get("content") or sec.get("desc")  or "").strip()
        points = sec.get("points") or sec.get("mains") or sec.get("items") or []
        mains: List[Dict[str, Any]] = []
        if isinstance(points, list):
            for p in points:
                if isinstance(p, dict):
                    mains.append({
                        "text": (p.get("main") or p.get("text") or p.get("title") or "").strip(),
                        "subs": [
                            (s if isinstance(s, str) else
                             (s.get("text") or s.get("title") or s.get("name") or "")
                            ) for s in (p.get("subs") or [])
                        ]
                    })
                elif isinstance(p, str):
                    mains.append({"text": p.strip(), "subs": []})
        yield title, body, mains


# ========================= ฟังก์ชันหลัก =========================
def doc_chapter5(intro_body: str, sections_json: List[Dict[str, Any]]) -> Document:
    """
    สร้างบทที่ 5 ให้ตรงคู่มือ:
    - ฟอนต์ TH SarabunPSK ขนาด 16pt, บรรทัด 1.0
    - หัวกลาง 2 บรรทัด (20pt หนา): 'บทที่ 5' และ 'สรุปผลการวิจัย อภิปรายผล และข้อเสนอแนะ'
    - ระยะกระดาษหน้าแรก: บน 2.0", ล่าง 1.0", ซ้าย 1.5", ขวา 1.0"
      แล้วสลับเป็น top 1.0" สำหรับหน้าถัดไปด้วย section แบบต่อเนื่อง
    - ย่อหน้าเนื้อหา: ใช้ add_wrapped_paragraph (tap=1.0 ซม.) หรือ custom_tap
    """
    doc = Document()

    # ตั้งฟอนต์/สไตล์เริ่มต้น
    style = doc.styles["Normal"]
    style.font.name = FONT_NAME
    style.element.rPr.rFonts.set(qn("w:eastAsia"), FONT_NAME)
    style.font.size = Pt(BASE_PT)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    # ตั้ง margin หน้าแรก
    section = doc.sections[0]
    section.top_margin = Inches(FIRST_TOP_INCH)
    section.bottom_margin = Inches(BOTTOM_INCH)
    section.left_margin = Inches(LEFT_INCH)
    section.right_margin = Inches(RIGHT_INCH)

    # ===== หัวเรื่องกลางหน้า =====
    add_center_paragraph(doc, "บทที่ 5", bold=True, font_size=TITLE_PT)
    add_center_paragraph(doc, "สรุปผลการวิจัย อภิปรายผล และข้อเสนอแนะ", bold=True, font_size=TITLE_PT)

    # เปลี่ยน top margin สำหรับหน้าถัดไปเป็น 1.0" (ไม่ขึ้นหน้าใหม่)
    _apply_rest_page_margin(doc, top_inch=REST_TOP_INCH)

    # ===== 5.1 บทนำ =====
    add_left_paragraph(doc, "5.1  บทนำ", bold=True)
    if (intro_body or "").strip():
        # ชิดซ้าย + ย่อบรรทัดแรก 1 ซม. + ตัดคำไทยรองรับ \t
        add_wrapped_paragraph(doc, intro_body, n=LINE_LEN, disth=True, tap=True)

    # ===== 5.2, 5.3, ... =====
    for i, (title, body, mains) in enumerate(_iter_sections(sections_json), start=2):
        # หัวข้อใหญ่ (ตัวหนา)
        add_left_paragraph(doc, f"5.{i}  {title}".strip(), bold=True)

        # เนื้อหาหัวข้อใหญ่
        if body:
            add_wrapped_paragraph(doc, body, n=LINE_LEN, disth=True, tap=True)

        # หัวข้อหลัก 5.i.j
        for j, m in enumerate(mains or [], start=1):
            main_text = (m.get("text") or "").strip()
            if main_text:
                # ตัวหนา และคงสไตล์ย่อหน้าไว้ให้ Word จัดบรรทัดเอง
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
