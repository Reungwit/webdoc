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
    
    
# ฟังก์ชัน จัดหัวข้อ หลัก/ย่อย รูปแบบข้อมูลJSON 
def iter_sections(sections: List[Dict[str, Any]]) -> Iterable[Tuple[str, str, List[Dict[str, Any]]]]:
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