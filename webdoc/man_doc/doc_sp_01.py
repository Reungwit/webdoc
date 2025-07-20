from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH 
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, Cm, Inches
def doc_sp_01(name_th, name_en):
    

    doc = Document()
    
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    # style.font.bold = True
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0
    style = doc.styles.add_style('StyleCenter', WD_STYLE_TYPE.PARAGRAPH)
    # ตั้งค่าขอบกระดาษ
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(0.8858)
    section.left_margin = Inches(1.248)
    section.right_margin = Inches(0.748)

    
    
    # doc.add_paragraph(content)
    head_1 = doc.add_paragraph("ทก.01")
    head_1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    head_1.style.font.bold = True
    
    
    add_center_paragraph(doc, "แบบเสนอโครงงานพิเศษ (ปริญญานิพนธ์)", bold=True)
    add_center_paragraph(doc, "ภาควิชาเทคโนโลยีสารสนเทศ" , bold=True)
    add_center_paragraph(doc, "คณะเทคโนโลยีและการจัดการอุตสาหกรรม" , bold=True)
    add_left_paragraph(doc , "1.ข้อมูลขั้นต้นของโครงงาน" , bold=True)
    p = doc.add_paragraph()
    p.add_run("1.1 ชื่อโครงงาน (ภาษาไทย)\t").bold = True
    p.add_run(name_th).bold = False
    add_paragraph_indent(doc, f"\t(ภาษาอังกฤษ)\t{name_en}")
    
   


    return doc

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
