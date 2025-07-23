    
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH 
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, Cm, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def doc_cover_th(name_pro_th, name_pro_en, authors,case_stu,term,school_y,adviser,co_advisor,strategic,plan,key_result):

    doc = docx.Document()
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    style.font.bold = True
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)

    doc.add_paragraph("").alignment = 1
    title = doc.add_paragraph(project_title_th)
    title.alignment = 1
    doc.add_paragraph(project_title_en).alignment = 1

    doc.add_paragraph("\n\n\n\n\n\n")
    doc.add_paragraph(f" {author_th_1}").alignment = 1
    doc.add_paragraph(f" {author_th_2}").alignment = 1
    doc.add_paragraph("\n\n\n\n\n\n\n\n")
    doc.add_paragraph("ปริญญานิพนธ์นี้เป็นส่วนหนึ่งของการศึกษาตามหลักสูตรอุตสาหกรรมศาสตรบัณฑิต").alignment = 1
    doc.add_paragraph("สาขาวิชาเทคโนโลยีสารสนเทศ ภาควิชาเทคโนโลยีสารสนเทศ").alignment = 1
    doc.add_paragraph("คณะเทคโนโลยีและการจัดการอุตสาหกรรม").alignment = 1
    doc.add_paragraph("มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ").alignment = 1
    doc.add_paragraph(f"ปีการศึกษา {academic_year}").alignment = 1
    doc.add_paragraph("ลิขสิทธิ์ของมหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ").alignment = 1

    return doc
