from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm

def set_font_style(run, font_name='Angsana New', font_size=16):
    """
    ฟังก์ชันช่วยตั้งค่าฟอนต์สำหรับ run ของ python-docx
    """
    run.font.name = font_name
    run.font.size = Pt(font_size)
    r = run._element
    r.rPr.rFonts.set(qn('w:eastAsia'), font_name)

def add_heading_th(document, text, font_size=20, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER):
    """
    ฟังก์ชันช่วยเพิ่มหัวข้อภาษาไทย
    """
    paragraph = document.add_paragraph()
    paragraph.alignment = alignment
    run = paragraph.add_run(text)
    set_font_style(run, font_name='Angsana New', font_size=font_size)
    run.bold = bold

def add_paragraph_with_indent(document, text, font_size=16, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY):
    """
    ฟังก์ชันช่วยเพิ่มย่อหน้าพร้อมระยะย่อหน้า
    """
    paragraph = document.add_paragraph(text)
    paragraph.alignment = alignment
    run = paragraph.runs[0]
    set_font_style(run, font_name='Angsana New', font_size=font_size)
    paragraph.paragraph_format.first_line_indent = Inches(0.5)
    paragraph.paragraph_format.line_spacing = 1.0

def add_paragraph_no_indent(document, text, font_size=16, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY):
    """
    ฟังก์ชันช่วยเพิ่มย่อหน้าแบบไม่มีระยะย่อหน้า
    """
    paragraph = document.add_paragraph(text)
    paragraph.alignment = alignment
    run = paragraph.runs[0]
    set_font_style(run, font_name='Angsana New', font_size=font_size)
    paragraph.paragraph_format.line_spacing = 1.0
    
def doc_intro(data):
    """
    ฟังก์ชันสำหรับสร้างไฟล์เอกสาร Word (.docx) ส่วนบทคัดย่อและกิตติกรรมประกาศ
    """
    # 1. สร้างเอกสารใหม่
    document = Document()
    
    # ตั้งค่าหน้ากระดาษเริ่มต้น (สำหรับทุกหน้า)
    section = document.sections[0]
    section.top_margin = Cm(3.81)  # 1.5 นิ้ว
    section.bottom_margin = Cm(2.54) # 1 นิ้ว
    section.left_margin = Cm(3.81)  # 1.5 นิ้ว
    section.right_margin = Cm(2.54) # 1 นิ้ว

    # 2. ส่วนของ บทคัดย่อภาษาไทย
    add_heading_th(document, "บทคัดย่อ")
    add_paragraph_with_indent(document, data.get('abstract_th_para1', ''), alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    p_keyword = document.add_paragraph()
    p_keyword.paragraph_format.line_spacing = 1.0
    run_keyword = p_keyword.add_run('คำสำคัญ: ')
    set_font_style(run_keyword, font_name='Angsana New', font_size=16)
    run_keyword_value = p_keyword.add_run(data.get('keyword_th', ''))
    set_font_style(run_keyword_value, font_name='Angsana New', font_size=16)
    
    # 3. ขึ้นหน้าใหม่สำหรับบทคัดย่อภาษาอังกฤษ
    document.add_page_break()
    add_heading_th(document, "ABSTRACT", bold=True)
    add_paragraph_with_indent(document, data.get('abstract_en_para1', ''), alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    p_keyword_en = document.add_paragraph()
    p_keyword_en.paragraph_format.line_spacing = 1.0
    run_keyword_en = p_keyword_en.add_run('Keywords: ')
    set_font_style(run_keyword_en, font_name='Angsana New', font_size=16)
    run_keyword_value_en = p_keyword_en.add_run(data.get('keyword_en', ''))
    set_font_style(run_keyword_value_en, font_name='Angsana New', font_size=16)
    
    # 4. ขึ้นหน้าใหม่สำหรับกิตติกรรมประกาศ
    document.add_page_break()
    add_heading_th(document, "กิตติกรรมประกาศ")
    add_paragraph_with_indent(document, data.get('acknow_para1', ''), alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_paragraph_with_indent(document, data.get('acknow_para2', ''), alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    # ชื่อผู้จัดทำ
    if data.get('acknow_name1', ''):
        p_author1 = document.add_paragraph()
        p_author1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_author1.paragraph_format.space_before = Pt(36)
        run_author1 = p_author1.add_run(f"({data.get('acknow_name1', '')})")
        set_font_style(run_author1, font_name='Angsana New', font_size=16)

    if data.get('acknow_name2', ''):
        p_author2 = document.add_paragraph()
        p_author2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_author2.paragraph_format.space_before = Pt(12)
        run_author2 = p_author2.add_run(f"({data.get('acknow_name2', '')})")
        set_font_style(run_author2, font_name='Angsana New', font_size=16)

    return documen