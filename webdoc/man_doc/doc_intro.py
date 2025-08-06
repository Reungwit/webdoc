# from docx import Document
# from docx.shared import Inches, Pt
# from docx.enum.text import WD_ALIGN_PARAGRAPH
# from docx.oxml.ns import qn
# from docx.shared import Cm

# def set_font_style(run, font_name='Angsana New', font_size=16):
#     """
#     ฟังก์ชันช่วยตั้งค่าฟอนต์สำหรับ run ของ python-docx
#     """
#     run.font.name = font_name
#     run.font.size = Pt(font_size)
#     r = run._element
#     r.rPr.rFonts.set(qn('w:eastAsia'), font_name)

# def add_heading_th(document, text, font_size=20, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER):
#     """
#     ฟังก์ชันช่วยเพิ่มหัวข้อภาษาไทย
#     """
#     paragraph = document.add_paragraph()
#     paragraph.alignment = alignment
#     run = paragraph.add_run(text)
#     set_font_style(run, font_name='Angsana New', font_size=font_size)
#     run.bold = bold

# def add_paragraph_with_indent(document, text, font_size=16, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY):
#     """
#     ฟังก์ชันช่วยเพิ่มย่อหน้าพร้อมระยะย่อหน้า
#     """
#     paragraph = document.add_paragraph(text)
#     paragraph.alignment = alignment
#     run = paragraph.runs[0]
#     set_font_style(run, font_name='Angsana New', font_size=font_size)
#     paragraph.paragraph_format.first_line_indent = Inches(0.5)
#     paragraph.paragraph_format.line_spacing = 1.0

# def add_paragraph_no_indent(document, text, font_size=16, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY):
#     """
#     ฟังก์ชันช่วยเพิ่มย่อหน้าแบบไม่มีระยะย่อหน้า
#     """
#     paragraph = document.add_paragraph(text)
#     paragraph.alignment = alignment
#     run = paragraph.runs[0]
#     set_font_style(run, font_name='Angsana New', font_size=font_size)
#     paragraph.paragraph_format.line_spacing = 1.0
    
# def doc_intro(data):
#     """
#     ฟังก์ชันสำหรับสร้างไฟล์เอกสาร Word (.docx) ส่วนบทคัดย่อและกิตติกรรมประกาศ
#     """
#     # 1. สร้างเอกสารใหม่
#     document = Document()
    
#     # ตั้งค่าหน้ากระดาษเริ่มต้น (สำหรับทุกหน้า)
#     section = document.sections[0]
#     section.top_margin = Cm(3.81)  # 1.5 นิ้ว
#     section.bottom_margin = Cm(2.54) # 1 นิ้ว
#     section.left_margin = Cm(3.81)  # 1.5 นิ้ว
#     section.right_margin = Cm(2.54) # 1 นิ้ว

#     # 2. ส่วนของ บทคัดย่อภาษาไทย
#     add_heading_th(document, "บทคัดย่อ")
#     add_paragraph_with_indent(document, data.get('abstract_th_para1', ''), alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
#     p_keyword = document.add_paragraph()
#     p_keyword.paragraph_format.line_spacing = 1.0
#     run_keyword = p_keyword.add_run('คำสำคัญ: ')
#     set_font_style(run_keyword, font_name='Angsana New', font_size=16)
#     run_keyword_value = p_keyword.add_run(data.get('keyword_th', ''))
#     set_font_style(run_keyword_value, font_name='Angsana New', font_size=16)
    
#     # 3. ขึ้นหน้าใหม่สำหรับบทคัดย่อภาษาอังกฤษ
#     document.add_page_break()
#     add_heading_th(document, "ABSTRACT", bold=True)
#     add_paragraph_with_indent(document, data.get('abstract_en_para1', ''), alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
#     p_keyword_en = document.add_paragraph()
#     p_keyword_en.paragraph_format.line_spacing = 1.0
#     run_keyword_en = p_keyword_en.add_run('Keywords: ')
#     set_font_style(run_keyword_en, font_name='Angsana New', font_size=16)
#     run_keyword_value_en = p_keyword_en.add_run(data.get('keyword_en', ''))
#     set_font_style(run_keyword_value_en, font_name='Angsana New', font_size=16)
    
#     # 4. ขึ้นหน้าใหม่สำหรับกิตติกรรมประกาศ
#     document.add_page_break()
#     add_heading_th(document, "กิตติกรรมประกาศ")
#     add_paragraph_with_indent(document, data.get('acknow_para1', ''), alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
#     add_paragraph_with_indent(document, data.get('acknow_para2', ''), alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
#     # ชื่อผู้จัดทำ
#     if data.get('acknow_name1', ''):
#         p_author1 = document.add_paragraph()
#         p_author1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
#         p_author1.paragraph_format.space_before = Pt(36)
#         run_author1 = p_author1.add_run(f"({data.get('acknow_name1', '')})")
#         set_font_style(run_author1, font_name='Angsana New', font_size=16)

#     if data.get('acknow_name2', ''):
#         p_author2 = document.add_paragraph()
#         p_author2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
#         p_author2.paragraph_format.space_before = Pt(12)
#         run_author2 = p_author2.add_run(f"({data.get('acknow_name2', '')})")
#         set_font_style(run_author2, font_name='Angsana New', font_size=16)

#     return document



# doc_intro.py
# doc_intro.py
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.section import WD_SECTION
from docx.document import Document as DocxDocument
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from pythainlp.tokenize import word_tokenize

def set_thai_distributed(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'thaiDistribute')
    p_pr.append(jc)

def add_center_paragraph(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        if p.runs:
            p.runs[0].bold = False
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

def add_paragraph_indent(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.paragraph_format.first_line_indent = Cm(1.27)
    if bold and p.runs:
        p.runs[0].bold = True
    else:
        if p.runs:
            p.runs[0].bold = False
    return p

def set_page_number_text(section, text):
    """
    ตั้งค่าเลขหน้าเป็นข้อความ 'ข', 'ค', 'ง' ที่ส่วนท้ายกระดาษ
    """
    footer = section.footer
    if not footer.paragraphs:
        footer.paragraphs.add()
    
    paragraph = footer.paragraphs[0]
    paragraph.text = text
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # ตั้งค่าฟอนต์สำหรับเลขหน้า
    for run in paragraph.runs:
        run.font.name = 'TH SarabunPSK'
        run.font.size = Pt(16)


def add_wrapped_paragraph(p_or_doc, text: str, n: int, disth: bool = False, extap: bool = False, tap: bool = False):
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
    words = word_tokenize(text, engine="newmm")
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

    # ตรวจสอบว่าเป็น doc/cell หรือ paragraph
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
    if extap:
        p.paragraph_format.first_line_indent = Cm(1.80)
    elif tap:
        p.paragraph_format.first_line_indent = Cm(1.27)
        
    return p


def doc_intro(data):
    """
    ฟังก์ชันสำหรับสร้างไฟล์เอกสาร Word (.docx) ส่วนบทคัดย่อและกิตติกรรมประกาศ
    """
    document = Document()
    
    # ตั้งค่าสไตล์เริ่มต้น (Normal Style)
    style = document.styles['Normal']
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    # ตั้งค่าหน้ากระดาษเริ่มต้น (สำหรับทุกหน้า)
    section = document.sections[0]
    section.top_margin = Cm(3.81)  # 1.5 นิ้ว
    section.bottom_margin = Cm(2.54) # 1 นิ้ว
    section.left_margin = Cm(3.81)  # 1.5 นิ้ว
    section.right_margin = Cm(2.54) # 1 นิ้ว

    # 1. สร้างหน้าบทคัดย่อภาษาไทย
    add_center_paragraph(document, "บทคัดย่อ", bold=True)
    add_wrapped_paragraph(document, data.get('abstract_th_para1', ''), n=93, disth=True, tap=True)
    add_wrapped_paragraph(document, data.get('abstract_th_para2', ''), n=93, disth=True, tap=True)

    p_keyword_th = add_left_paragraph(document, f"คำสำคัญ: {data.get('keyword_th', '')}")
    p_keyword_th.paragraph_format.space_before = Pt(12)
    
    # 2. ขึ้นหน้าใหม่สำหรับบทคัดย่อภาษาอังกฤษ
    document.add_section(WD_SECTION.NEW_PAGE)
    add_center_paragraph(document, "ABSTRACT", bold=True)
    add_wrapped_paragraph(document, data.get('abstract_en_para1', ''), n=93, disth=True, tap=True)
    add_wrapped_paragraph(document, data.get('abstract_en_para2', ''), n=93, disth=True, tap=True)
    
    p_keyword_en = add_left_paragraph(document, f"Keywords: {data.get('keyword_en', '')}")
    p_keyword_en.paragraph_format.space_before = Pt(12)

    # 3. ขึ้นหน้าใหม่สำหรับกิตติกรรมประกาศ
    document.add_section(WD_SECTION.NEW_PAGE)
    add_center_paragraph(document, "กิตติกรรมประกาศ", bold=True)
    p_acknow1 = add_wrapped_paragraph(document, data.get('acknow_para1', ''), n=93, disth=True, tap=True)
    p_acknow2 = add_wrapped_paragraph(document, data.get('acknow_para2', ''), n=93, disth=True, tap=True)

    
    # ชื่อผู้จัดทำ
    if data.get('acknow_name1', ''):
        p_author1 = add_right_paragraph(document, f"({data.get('acknow_name1', '')})")
        p_author1.paragraph_format.space_before = Pt(36)

    if data.get('acknow_name2', ''):
        p_author2 = add_right_paragraph(document, f"({data.get('acknow_name2', '')})")
        p_author2.paragraph_format.space_before = Pt(12)

    return document