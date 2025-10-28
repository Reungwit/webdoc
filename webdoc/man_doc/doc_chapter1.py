from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH 
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, Cm, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_BREAK # เหมือนกด Ctrl + Enter ใน Word
from docx.enum.section import WD_SECTION
from pythainlp.tokenize import word_tokenize #ใช้ตัดคำ
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from docx.document import Document as DocxDocument
def doc_chapter1(sec11_p1,sec11_p2,sec11_p3,purpose_count,purpose_1,purpose_2,purpose_3,hypo_paragraph,
                hypo_items,scope_data,para_premise_str,premise_data,def_items,benefit_items):
    
    doc = Document()

    # กำหนดรูปแบบฟอนต์สำหรับเอกสาร
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    # ตั้งค่าขอบกระดาษ
    section = doc.sections[0]
    section.top_margin = Inches(2.0)  # กำหนด margin หน้าแรก
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1)

     
  
        
    add_center_paragraph(doc, "บทที่ 1", bold=True ,font_size=20)
    add_center_paragraph(doc, "บทนำ\n", bold=True , font_size=20)

    # ส่วนที่ 1.1 ความเป็นมาและความสำคัญของปัญหา
    add_left_paragraph(doc, "1.1  ความเป็นมาและความสำคัญของปัญหา", bold=True)
    add_wrapped_paragraph(doc, sec11_p1, n=85, disth=True ,custom_tap=0.8)
    add_wrapped_paragraph(doc, sec11_p2, n=85, disth=True ,custom_tap=0.8)
    add_wrapped_paragraph(doc, sec11_p3, n=85, disth=True ,custom_tap=0.8)
    doc.add_paragraph()
    
    # วัตถุประสงค์
    add_left_paragraph(doc, "1.2  วัตถุประสงค์", bold=True)
    add_paragraph_indent(doc, f"1.2.1  {purpose_1}",custom_tap=0.8)
    add_paragraph_indent(doc, f"1.2.2  {purpose_2}",custom_tap=0.8)
    add_paragraph_indent(doc, f"1.2.3  {purpose_3}",custom_tap=0.8)
    add_page_break(doc ,1.5)
    
    # ส่วนที่เกี่ยวข้องกับ Hypothesis (สมมติฐาน)
    add_left_paragraph(doc, "1.3  สมมติฐาน", bold=True )
    add_wrapped_paragraph(doc, hypo_paragraph, n=85, disth=True,custom_tap=0.8)
    for i, item in enumerate(hypo_items, start=1):
        if isinstance(item, dict):
            txt = (item.get("main") or "").strip()
        else:
            txt = (item or "").strip()
        if txt:
            add_paragraph_indent(doc, f"1.3.{i}  {txt}",custom_tap=0.8)
            
    doc.add_paragraph()
    # ขอบเขตการทำงาน เหลือจัดระยะให้ถูกต้อง
    add_left_paragraph(doc, "1.4  ขอบเขตการทำโครงงาน", bold=True)
    for i, item in enumerate(scope_data, start=1):
        main = item.get('main', '').strip()
        if main:
            add_paragraph_indent(doc, f"1.4.{i}  {main}")  # แสดงข้อมูล main
        for j, sub in enumerate(item.get('subs', []), start=1):
            sub = sub.strip()
            if sub:
                add_paragraph_indent(doc, f"\t1.4.{i}.{j}  {sub}")  # แสดงข้อมูล sub
    
    add_page_break(doc ,1.5)

    # ข้อตกลงเบื้องต้น
    add_left_paragraph(doc, "1.5  ข้อตกลงเบื้องต้น", bold=True)
    add_wrapped_paragraph(doc, para_premise_str, n=85, disth=True,custom_tap=0.8)
    for i, item in enumerate(premise_data, start=1):
        main = item.get('main', '').strip()
        if main:
            add_paragraph_indent(doc, f"1.5.{i}  {main}")  # แสดงข้อมูล main
        for j, sub in enumerate(item.get('subs', []), start=1):
            sub = sub.strip()
            if sub:
                add_paragraph_indent(doc, f"\t1.5.{i}.{j}  {sub}")  # แสดงข้อมูล sub
    doc.add_paragraph()

    # นิยามศัพท์เฉพาะ
    add_left_paragraph(doc, "1.6  นิยามศัพท์เฉพาะ", bold=True)
    for i, item in enumerate(def_items, start=1):
        if isinstance(item, dict):
            txt = (item.get("main") or "").strip()
        else:
            txt = (item or "").strip()
        if txt:
            add_paragraph_indent(doc, f"1.5.{i}  {txt}",custom_tap=0.8)
    
    doc.add_paragraph()

    add_left_paragraph(doc, "1.7  ประโยชน์ที่คาดว่าจะได้รับ", bold=True)
    for i, item in enumerate(benefit_items, start=1):
        if isinstance(item, dict):
            txt = (item.get("main") or "").strip()
        else:
            txt = (item or "").strip()
        if txt:
            add_paragraph_indent(doc, f"1.7.{i}  {txt}",custom_tap=0.8)
            
            
            
            
            
            
            
            
            
            
    return doc

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
    else : p.runs[0].bold = False
    return p

def add_paragraph_indent(doc, text, bold=False, custom_tap: float = 0.0):
    p = doc.add_paragraph(text)
    if bold and p.runs:
        p.runs[0].bold = True
    else : p.runs[0].bold = False
    
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
    # doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # เพิ่ม section break แบบเริ่มหน้าถัดไป
    new_section = doc.add_section(WD_SECTION.NEW_PAGE)
    # ตั้งค่า margin เฉพาะ section นี้
    new_section.top_margin = Inches(top_margin_inch)