from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH 
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, Cm, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def doc_sp_01(name_pro_th, name_pro_en, authors,case_stu,term,school_y,adviser,co_advisor,strategic,plan,key_result):
    

    doc = Document()
    
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    # style.font.bold = True
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0
    # ตั้งค่าขอบกระดาษ
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(0.8858)
    section.left_margin = Inches(1.248)
    section.right_margin = Inches(0.748)
    add_page_number(section)

    
    
    head_1 = doc.add_paragraph("ทก.01")
    head_1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    head_1.runs[0].bold = True
    
    
    add_center_paragraph(doc, "แบบเสนอโครงงานพิเศษ (ปริญญานิพนธ์)", bold=True)
    add_center_paragraph(doc, "ภาควิชาเทคโนโลยีสารสนเทศ", bold=True)
    add_center_paragraph(doc, "คณะเทคโนโลยีและการจัดการอุตสาหกรรม" , bold=True)
    add_left_paragraph(doc , "1.ข้อมูลขั้นต้นของโครงงาน" , bold=True)
    p = doc.add_paragraph()
    p.add_run("\t1.1 ชื่อโครงงาน (ภาษาไทย)\t").bold = True
    p.add_run(name_pro_th).bold = False
    add_paragraph_indent(doc, f"\t\t(ภาษาอังกฤษ)\t{name_pro_en}")
    p = doc.add_paragraph()
    p.add_run(f"\t\tกรณีศึกษา").bold = True
    p.add_run(f" (ถ้ามี)\t{case_stu}\n").bold = False
    add_paragraph_indent(doc ,"1.2 ชื่อนักศึกษาผู้ทำโครงงาน",bold=True)
    
    # รายชื่อแต่ละคน
    for idx, name in enumerate(authors, start=1):
        add_paragraph_indent(doc,f"\t{idx}. {name}",bold=False)
        # sub_p.paragraph_format.left_indent = Cm(1.5)  # ขยับย่อหน้า
    doc.add_paragraph("")
    add_paragraph_indent(doc ,"\tหลักสูตรอุตสาหกรรมศาสตรบัณฑิต   ภาควิชาเทคโนโลยีสารสนเทศ (ต่อเนื่อง)",bold=False)
    add_paragraph_indent(doc ,f"\tภาคเรียนที่\t{term}\tปีการศึกษา {school_y} ",bold=False)
    doc.add_paragraph("")
    add_paragraph_indent(doc , "1.3 ชื่ออาจารย์ที่ปรึกษา ", bold=True)
    add_paragraph_indent(doc , f"\t\t{adviser}", bold=False)
    add_paragraph_indent(doc , "     อาจารย์ที่ปรึกษาร่วม ", bold=True)
    add_paragraph_indent(doc , f"\t\t{co_advisor}\n", bold=False)
    add_paragraph_indent(doc , "1.4 ความสอดคล้องกับแผนงานด้านวิทยศาสตร์ วิจัยละนวัตกรรม", bold=True)
    
    
    p = doc.add_paragraph()
    p.add_run(f"\tยุทธศาสตร์ที่ ").bold = True
    wrapped = split_text_newline_every_n_words(strategic, n=16)
    p.add_run(wrapped)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_thai_distributed(p)

    p = doc.add_paragraph()
    p.add_run(f"\tแผนงานที่ (P) ").bold = True
    wrapped = split_text_newline_every_n_words(plan, n=16)
    p.add_run(wrapped)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    # set_thai_distributed(p)

    p = doc.add_paragraph()
    p.add_run(f"\tผลลัพธ์ที่สำคัญ (key result) ").bold = True
    wrapped = split_text_newline_every_n_words(key_result, n=16)
    p.add_run(wrapped)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    # set_thai_distributed(p)

    




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
            p.add_run().add_break()         # ✅ บรรทัดใหม่จริง
            p.add_run(line)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
