from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH 
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, Cm, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


#หน้าปกไทย
def doc_cover_th( project_name_th, project_name_en,
                author1_th, author2_th,
                author1_en, author2_en,
                school_y):

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    style.font.bold = True
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0
    # ตั้งค่าขอบกระดาษ
    section = doc.sections[0]
    section.top_margin = Inches(1.5)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1)

    # ดึง path รูปภาพ (สมมุติแหม่มวางไว้ในโฟลเดอร์ static/images/)
    logo_path = os.path.join('static', 'img', 'kmutnb_logo_cover.png')

# แทรกรูปภาพ
    doc.add_picture(logo_path, width=Inches(1.7))

# จัดรูปให้อยู่ตรงกลาง
    last_paragraph = doc.paragraphs[-1]            
    last_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # add_page_number(section)
    doc.add_paragraph("").alignment = 1
    title = doc.add_paragraph(project_name_th)
    title.alignment = 1
    doc.add_paragraph(project_name_en).alignment = 1


    doc.add_paragraph("\n\n\n\n\n\n")
    doc.add_paragraph(f" {author1_th}").alignment = 1
    doc.add_paragraph(f" {author2_th}").alignment = 1
    doc.add_paragraph("\n\n\n\n")
    doc.add_paragraph("ปริญญานิพนธ์นี้เป็นส่วนหนึ่งของการศึกษาตามหลักสูตรอุตสาหกรรมศาสตรบัณฑิต").alignment = 1
    doc.add_paragraph("สาขาวิชาเทคโนโลยีสารสนเทศ ภาควิชาเทคโนโลยีสารสนเทศ").alignment = 1
    doc.add_paragraph("คณะเทคโนโลยีและการจัดการอุตสาหกรรม").alignment = 1
    doc.add_paragraph("มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ").alignment = 1
    doc.add_paragraph(f"ปีการศึกษา {academic_year}").alignment = 1
    doc.add_paragraph("ลิขสิทธิ์ของมหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ").alignment = 1

    return doc

#หน้าปกรอง
def doc_cover_sec( project_name_th, project_name_en,
                author1_th, author2_th,
                author1_en, author2_en,
                academic_year):

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    #style.font.bold = True
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0
    # ตั้งค่าขอบกระดาษ
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1)

    # add_page_number(section)
    doc.add_paragraph("").alignment = 1
    title = doc.add_paragraph(project_name_th)
    title.alignment = 1
    doc.add_paragraph(project_name_en).alignment = 1


    doc.add_paragraph("\n\n\n\n\n\n\n\n")
    doc.add_paragraph(f" {author1_th}").alignment = 1
    doc.add_paragraph(f" {author2_th}").alignment = 1
    doc.add_paragraph("\n\n\n\n\n\n\n\n")
    doc.add_paragraph("ปริญญานิพนธ์นี้เป็นส่วนหนึ่งของการศึกษาตามหลักสูตรอุตสาหกรรมศาสตรบัณฑิต").alignment = 1
    doc.add_paragraph("สาขาวิชาเทคโนโลยีสารสนเทศ ภาควิชาเทคโนโลยีสารสนเทศ").alignment = 1
    doc.add_paragraph("คณะเทคโนโลยีและการจัดการอุตสาหกรรม").alignment = 1
    doc.add_paragraph("มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ").alignment = 1
    doc.add_paragraph(f"ปีการศึกษา {academic_year}").alignment = 1
    doc.add_paragraph("ลิขสิทธิ์ของมหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ").alignment = 1

    return doc
#หน้าปกภาษาอังกฤษ
def doc_cover_en(project_name_th, project_name_en,
                 author1_th, author2_th,
                 author1_en, author2_en,
                 academic_year):

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    #style.font.bold = True
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1)

    doc.add_paragraph("").alignment = 1
    title = doc.add_paragraph(project_name_en)
    title.alignment = 1

    doc.add_paragraph("\n\n\n\n\n\n\n\n")
    doc.add_paragraph(f"{author1_en}").alignment = 1
    doc.add_paragraph(f"{author2_en}").alignment = 1
    doc.add_paragraph("\n\n\n\n\n\n\n\n")
    doc.add_paragraph("PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS").alignment = 1
    doc.add_paragraph("FOR THE BACHELOR’S DEGREE OF INDUSTRIAL TECHNOLOGY").alignment = 1
    doc.add_paragraph("PROGRAM IN INFORMATION TECHNOLOGY").alignment = 1
    doc.add_paragraph("DEPARTMENT OF INFORMATION TECHNOLOGY").alignment = 1
    doc.add_paragraph("FACULTY OF INDUSTRIAL TECHNOLOGY AND MANAGEMENT").alignment = 1
    doc.add_paragraph("KING MONGKUT'S UNIVERSITY OF TECHNOLOGY NORTH BANGKOK").alignment = 1

    # ✅ แปลงปี พ.ศ. → ค.ศ. ด้วยการลด 543
    try:
        academic_year_int = int(academic_year)
        gregorian_year = academic_year_int - 543
        doc.add_paragraph(f"ACADEMIC YEAR {gregorian_year}").alignment = 1
    except:
        doc.add_paragraph("ACADEMIC YEAR (____)").alignment = 1

    doc.add_paragraph("COPYRIGHT OF KING MONGKUT'S UNIVERSITY OF TECHNOLOGY NORTH BANGKOK").alignment = 1

    return doc

def add_page_number(section):
    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = 1  # 0=left, 1=center, 2=right

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
    p_pr = paragraph._p.get_or_add_pPr()
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'thaiDistribute')
    p_pr.append(jc)

def split_text_newline_every_n_words(text, n):
    words = text.split()
    lines = [" ".join(words[i:i+n]) for i in range(0, len(words), n)]
    return (lines)


def add_center_paragraph(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if bold and p.runs:
        p.runs[0].bold = True
    else : p.runs[0].bold = False
    return p

def add_left_paragraph(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if bold and p.runs:
        p.runs[0].bold = True
    else : p.runs[0].bold = False
    return p

def add_right_paragraph(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if bold and p.runs:
        p.runs[0].bold = True
    else : p.runs[0].bold = False
    return p

def add_paragraph_indent(doc, text, bold=False):
    p = doc.add_paragraph(text)
    p.paragraph_format.first_line_indent = Cm(1.27)
    if bold and p.runs:
        p.runs[0].bold = True
    else : p.runs[0].bold = False
    return p

def add_wrapped_paragraph(doc, label, text, n=16):
    lines = split_text_newline_every_n_words(text, n)

    p = doc.add_paragraph()
    run = p.add_run(label)
    run.bold = True

    # ต่อข้อความแบบขึ้นบรรทัดใหม่ทีละ run
    for i, line in enumerate(lines):
        if i == 0:
            p.add_run(line)
        else:
            p.add_run().add_break()         # บรรทัดใหม่จริง
            p.add_run(line)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY