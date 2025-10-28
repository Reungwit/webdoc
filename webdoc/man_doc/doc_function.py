from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.section import WD_SECTION
from pythainlp.tokenize import word_tokenize  # ใช้ตัดคำภาษาไทย
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from docx.document import Document as DocxDocument

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from docx.shared import Inches
from docx.enum.section import WD_SECTION


def doc_setup():
    """
    ฟังก์ชันสร้าง Document ใหม่ และตั้งค่ารูปแบบฟอนต์ + หน้ากระดาษพื้นฐาน
    ใช้สำหรับเริ่มต้นสร้างเอกสารใหม่ให้มีมาตรฐานเดียวกันในทุกบท
    """
    doc = Document()

    # ตั้งค่ารูปแบบฟอนต์พื้นฐาน
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    # ตั้งค่าหน้ากระดาษ
    section = doc.sections[0]
    section.top_margin = Inches(2.0)     # margin ด้านบน
    section.bottom_margin = Inches(1.0)  # margin ด้านล่าง
    section.left_margin = Inches(1.5)    # margin ซ้าย
    section.right_margin = Inches(1.0)   # margin ขวา

    return doc


def add_center_paragraph(doc, text, bold=False, font_size=16):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        if p.runs:
            p.runs[0].bold = False
    if p.runs:
        p.runs[0].font.size = Pt(font_size)
    return p


def add_left_paragraph(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        if p.runs:
            p.runs[0].bold = False
    return p


def add_right_paragraph(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        if p.runs:
            p.runs[0].bold = False
    return p


def add_paragraph_indent(doc, text, bold=False, custom_tap: float = 0.0):
    p = doc.add_paragraph(text)
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        if p.runs:
            p.runs[0].bold = False

    if custom_tap:
        p.paragraph_format.first_line_indent = Cm(custom_tap)
    else:
        p.paragraph_format.first_line_indent = Cm(1.00)
    return p


def add_wrapped_paragraph(
    p_or_doc,
    text: str,
    n: int,
    disth: bool = False,
    extap: bool = False,
    tap: bool = False,
    custom_tap: float = 0.0
):
    """
    สร้างหรือเพิ่มข้อความที่ถูกตัดคำลงใน paragraph หรือ document/cell
    disth=True จะใช้ thaiDistribute แทน justify
    """

    def set_thai_distributed(paragraph):
        p_pr = paragraph._p.get_or_add_pPr()
        jc = OxmlElement('w:jc')
        jc.set(qn('w:val'), 'thaiDistribute')
        p_pr.append(jc)

    # แบ่งบรรทัดภาษาไทยตามความยาว n
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

    # ตรวจชนิดอาร์กิวเมนต์
    if isinstance(p_or_doc, (DocxDocument, _Cell)):
        p = p_or_doc.add_paragraph()
    elif isinstance(p_or_doc, Paragraph):
        p = p_or_doc
    else:
        raise TypeError("Argument must be Document, _Cell, or Paragraph")

    # เพิ่มข้อความทีละบรรทัด
    for idx, l in enumerate(lines):
        tab_count = len(l) - len(l.lstrip("\t"))
        l = l.lstrip("\t")

        # ใส่ tab ตามจำนวน
        for _ in range(tab_count):
            p.add_run().add_tab()

        # ใส่ข้อความที่เหลือ
        if l.strip():
            p.add_run(l)

        if idx < len(lines) - 1:
            p.add_run().add_break()

    # รูปแบบย่อหน้า
    p.paragraph_format.keep_together = True
    p.paragraph_format.keep_with_next = True

    if disth:
        set_thai_distributed(p)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ระยะย่อหน้าแรก
    if extap:
        p.paragraph_format.first_line_indent = Cm(1.80)
    elif tap:
        p.paragraph_format.first_line_indent = Cm(1.00)
    elif custom_tap:
        p.paragraph_format.first_line_indent = Cm(custom_tap)

    return p


def add_page_break(doc, top_margin_inch=1.5):
    """
    แทรก Section Break (New Page) แล้วตั้งค่า margin บนของหน้าถัดไป
    """
    new_section = doc.add_section(WD_SECTION.NEW_PAGE)
    new_section.top_margin = Inches(top_margin_inch)



#จากไฟล์cover
def add_page_number(section, align: str = "center"):
    """
    แทรกเลขหน้า (PAGE field) ที่ footer ของ section ที่กำหนด
    align: 'left' | 'center' | 'right'
    """
    align_map = {"left": 0, "center": 1, "right": 2}
    footer = section.footer
    paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    paragraph.alignment = align_map.get(align, 1)

    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')

    fldChar3 = OxmlElement('w:t')
    fldChar3.text = "1"

    fldChar4 = OxmlElement('w:fldChar')
    fldChar4.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)
    run._r.append(fldChar4)

def set_thai_distributed(paragraph):
    """
    ตั้ง alignment เป็น thaiDistribute สำหรับย่อหน้าที่ต้องการกระจายตัวอักษรภาษาไทย
    """
    p_pr = paragraph._p.get_or_add_pPr()
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'thaiDistribute')
    p_pr.append(jc)

def split_text_newline_every_n_words(text: str, n: int):
    """
    แยกสตริงเป็นบรรทัดใหม่ทุก ๆ n คำ (เว้นวรรคเป็นตัวแบ่ง)
    """
    words = text.split()
    lines = [" ".join(words[i:i+n]) for i in range(0, len(words), n)]
    return lines



# --- บท5 ---
# ใช้ร่วมกับทุกบท: เปลี่ยน top margin สำหรับหน้าถัดไป "แบบไม่ขึ้นหน้าใหม่"
def apply_rest_page_margin(doc, *, top_inch: float = 1.0, left_inch: float = 1.5, right_inch: float = 1.0, bottom_inch: float = 1.0):
    """
    แทรก Section แบบ CONTINUOUS แล้วตั้งค่า margin สำหรับเนื้อหาหน้าถัดไป
    เหมาะกับกรณี: หน้าแรก top 2.0", หน้าอื่น ๆ top 1.0" เป็นต้น
    """
    sec = doc.add_section(WD_SECTION.CONTINUOUS)
    sec.top_margin = Inches(top_inch)
    sec.bottom_margin = Inches(bottom_inch)
    sec.left_margin = Inches(left_inch)
    sec.right_margin = Inches(right_inch)
