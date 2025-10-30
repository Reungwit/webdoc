from __future__ import annotations
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
from typing import Any, Dict, Iterable, List, Tuple, Optional
import json


def doc_setup():
    doc = Document()

    # กำหนดรูปแบบฟอนต์สำหรับเอกสาร
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    # ✅ ใช้ first section แบบปลอดภัย (กัน edge-case)
    section = doc.sections[0] if getattr(doc, "sections", None) and len(doc.sections) > 0 \
              else doc.add_section(WD_SECTION.NEW_PAGE)

    section.top_margin    = Inches(2.0)  # กำหนด margin หน้าแรก
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.5)
    section.right_margin  = Inches(1)

    return doc

def add_center_paragraph(doc, text, bold=False, font_size=16):
    p = doc.add_paragraph()
    r = p.add_run(text or "")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r.bold = bool(bold)
    r.font.size = Pt(font_size)
    return p

def add_left_paragraph(doc, text, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text or "")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r.bold = bool(bold)
    return p

def add_right_paragraph(doc, text, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text or "")
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r.bold = bool(bold)
    return p


def add_paragraph_indent(doc, text, bold=False, custom_tap: float = 0.0):
    p = doc.add_paragraph()
    r = p.add_run(text or "")
    r.bold = bool(bold)
    p.paragraph_format.first_line_indent = Cm(custom_tap if custom_tap else 1.00)
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




# ---------- helpers ----------
def _t(v: Any) -> str:
    return (v or "").strip() if isinstance(v, str) else ""

def _safe_parse_list(raw: Any, fallback: list = None) -> list:
    if isinstance(raw, list):
        return raw
    try:
        data = json.loads(raw or "[]")
        return data if isinstance(data, list) else (fallback or [])
    except Exception:
        return fallback or []

def _default_sections_for_ui() -> List[Dict[str, Any]]:
    # UI ต้องการหัวข้อแรกแบบ paragraphs, ที่เหลือใช้ body+points
    out: List[Dict[str, Any]] = []
    for i, t in enumerate(DEFAULT_TITLES):
        if i == 0:
            out.append({"title": t, "paragraphs": [], "points": []})
        else:
            out.append({"title": t, "body": "", "points": []})
    return out


# ---------- 1) iterator กลาง: คืน (title, body, mains) ----------
def iter_sections(sections_any: Any,*,first_section_mode: str = "paragraphs",  ) -> Iterable[Tuple[str, str, List[Dict[str, Any]]]]:
    """
    รับ schema ได้หลายแบบจาก UI/DB แล้ว 'normalize' ให้เป็น:
      - title: str
      - body: str
      - mains: List[{"text": str, "subs": List[str]}]
    โดย:
      - ถ้า first_section_mode == "paragraphs": หัวข้อแรกใช้ paragraphs (แต่จะคืน body="" และ mains=[])
      - หัวข้ออื่น ๆ แปลง points->mains ได้
    """
    sections = _safe_parse_list(sections_any, [])
    for i, sec in enumerate(sections):
        if not isinstance(sec, dict):
            continue

        title = _t(sec.get("title") or sec.get("header") or sec.get("name"))
        body  = _t(sec.get("body") or sec.get("content") or sec.get("desc"))

        # mains รับได้ทั้ง mains/points/items
        points = sec.get("mains")
        if not isinstance(points, list):
            points = sec.get("points")
        if not isinstance(points, list):
            points = sec.get("items")
        points = points if isinstance(points, list) else []

        mains: List[Dict[str, Any]] = []
        for p in points:
            if isinstance(p, dict):
                text = _t(p.get("text") or p.get("main") or p.get("title") or p.get("name"))
                subs_in = p.get("subs") if isinstance(p.get("subs"), list) else []
                subs = [_t(s if isinstance(s, str) else (s.get("text") if isinstance(s, dict) else "")) for s in subs_in]
                mains.append({"text": text, "subs": [s for s in subs if s]})
            elif isinstance(p, str):
                mains.append({"text": _t(p), "subs": []})

        # หัวข้อแรกแบบ paragraphs: ไม่คืน mains; body สำหรับหัวข้อแรกคงปล่อยว่างไป
        if i == 0 and first_section_mode == "paragraphs":
            yield (title, "", [])   # เนื้อหาย่อหน้าใหญ่ให้ไปอ่านจาก sec["paragraphs"] ฝั่งเอกสาร
        else:
            yield (title, body, mains)

# ---------- 2) UI -> DB (เซฟเป็น mains คงที่ ใช้ได้ทุกบท) ----------
def sections_db_from_ui(
    ui_any: Any,
    *,
    default_titles: Optional[List[str]] = None,
    first_section_mode: str = "paragraphs",  # "paragraphs" | "body"
) -> List[Dict[str, Any]]:
    ui = _safe_parse_list(ui_any, [])
    out: List[Dict[str, Any]] = []

    for i, sec in enumerate(ui):
        if not isinstance(sec, dict):
            continue
        title = _t(sec.get("title") or (default_titles[i] if default_titles and i < len(default_titles) else ""))

        if i == 0 and first_section_mode == "paragraphs":
            # บทที่ 1 (หรือบทไหนก็ตามที่อยากใช้ paragraphs)
            paras_in = sec.get("paragraphs")
            paras = []
            if isinstance(paras_in, list):
                for it in paras_in:
                    s = _t(it if isinstance(it, str) else (it.get("text") if isinstance(it, dict) else ""))
                    if s: paras.append(s)
            body = "\n\n".join(paras)  # เก็บ body ไว้เผื่อระบบเก่า
            out.append({"title": title, "paragraphs": paras, "body": body, "mains": []})
            continue

        # ที่เหลือ: normalize เป็น mains เสมอ (รองรับ points/mains)
        body = _t(sec.get("body"))
        mains_out: List[Dict[str, Any]] = []

        if isinstance(sec.get("mains"), list) and sec["mains"]:
            for m in sec["mains"]:
                if not isinstance(m, dict): continue
                text = _t(m.get("text") or m.get("title") or m.get("name"))
                subs_in = m.get("subs") if isinstance(m.get("subs"), list) else []
                subs = [_t(s if isinstance(s, str) else (s.get("text") if isinstance(s, dict) else "")) for s in subs_in]
                mains_out.append({"text": text, "subs": [x for x in subs if x]})
        elif isinstance(sec.get("points"), list):
            for p in sec["points"]:
                if isinstance(p, dict):
                    text = _t(p.get("main") or p.get("text") or p.get("title"))
                    subs_in = p.get("subs") if isinstance(p.get("subs"), list) else []
                    subs = [_t(s if isinstance(s, str) else (s.get("text") if isinstance(s, dict) else "")) for s in subs_in]
                    mains_out.append({"text": text, "subs": [x for x in subs if x]})
                elif isinstance(p, str):
                    txt = _t(p)
                    if txt: mains_out.append({"text": txt, "subs": []})

        out.append({"title": title, "body": body, "mains": mains_out})

    return out

# ---------- 3) DB -> UI (คืน schema เดิมสำหรับฟอร์ม: หัวข้อแรก paragraphs, ที่เหลือ body+points) ----------
def sections_ui_from_db(
    db_any: Any,
    *,
    default_titles: Optional[List[str]] = None,
    first_section_mode: str = "paragraphs",
) -> List[Dict[str, Any]]:
    db = _safe_parse_list(db_any, [])

    # เตรียมโครง UI ตามหัวข้อ
    ui: List[Dict[str, Any]] = []
    total = max(len(db), len(default_titles or []))
    for i in range(total or 1):
        t = (default_titles[i] if default_titles and i < len(default_titles) else "")
        if i == 0 and first_section_mode == "paragraphs":
            ui.append({"title": t, "paragraphs": [], "points": []})
        else:
            ui.append({"title": t, "body": "", "points": []})

    for i, sec in enumerate(db):
        if not isinstance(sec, dict) or i >= len(ui):
            continue
        title = _t(sec.get("title") or (default_titles[i] if default_titles and i < len(default_titles) else ""))

        if i == 0 and first_section_mode == "paragraphs":
            paras = []
            if isinstance(sec.get("paragraphs"), list) and sec["paragraphs"]:
                for it in sec["paragraphs"]:
                    s = _t(it if isinstance(it, str) else (it.get("text") if isinstance(it, dict) else ""))
                    if s: paras.append(s)
            else:
                body = _t(sec.get("body"))
                if body:
                    paras = [p.strip() for p in body.replace("\r\n", "\n").split("\n\n") if p.strip()]
            ui[i]["title"] = title
            ui[i]["paragraphs"] = paras
            continue

        ui[i]["title"] = title
        ui[i]["body"] = _t(sec.get("body"))
        points = []
        mains = sec.get("mains") if isinstance(sec.get("mains"), list) else []
        for m in mains:
            if not isinstance(m, dict): 
                if isinstance(m, str):
                    points.append({"main": _t(m), "subs": []})
                continue
            main_text = _t(m.get("text") or m.get("title") or m.get("name"))
            subs_out = []
            subs = m.get("subs") if isinstance(m.get("subs"), list) else []
            for s in subs:
                subs_out.append(_t(s if isinstance(s, str) else (s.get("text") if isinstance(s, dict) else "")))
            points.append({"main": main_text, "subs": [x for x in subs_out if x]})
        ui[i]["points"] = points

    return ui

# ---------- 4) สำหรับเอนจินเอกสาร: ค้ำประกันโครงสร้างก่อน render ----------
def sections_doc_safe(
    sections_any: Any,
    *,
    default_titles: List[str],
    first_section_mode: str = "paragraphs",
) -> List[Dict[str, Any]]:
    
    raw = _safe_parse_list(sections_any, [])
    want_n = len(default_titles or [])

    out: List[Dict[str, Any]] = []
    for i in range(want_n or 1):
        t = default_titles[i] if default_titles and i < len(default_titles) else ""
        if i == 0 and first_section_mode == "paragraphs":
            out.append({"title": t, "body": "", "paragraphs": [], "mains": []})
        else:
            out.append({"title": t, "body": "", "mains": []})

    for i in range(min(len(raw), len(out))):
        src = raw[i] if isinstance(raw[i], dict) else {}
        title = _t(src.get("title") or out[i]["title"])
        body  = _t(src.get("body"))

        if i == 0 and first_section_mode == "paragraphs":
            paras = []
            if isinstance(src.get("paragraphs"), list):
                for p in src["paragraphs"]:
                    s = _t(p if isinstance(p, str) else (p.get("text") if isinstance(p, dict) else ""))
                    if s: paras.append(s)
            if not paras and body:
                paras = [p.strip() for p in body.replace("\r\n","\n").split("\n\n") if p.strip()]
            out[i].update({"title": title, "body": body, "paragraphs": paras, "mains": []})
        else:
            mains_out = []
            mains_in = src.get("mains") if isinstance(src.get("mains"), list) else []
            for m in mains_in:
                if isinstance(m, dict):
                    text = _t(m.get("text") or m.get("title") or m.get("name"))
                    subs_in = m.get("subs") if isinstance(m.get("subs"), list) else []
                    subs = [_t(s if isinstance(s, str) else (s.get("text") if isinstance(s, dict) else "")) for s in subs_in]
                    mains_out.append({"text": text, "subs": [x for x in subs if x]})
                elif isinstance(m, str):
                    mains_out.append({"text": _t(m), "subs": []})
            out[i].update({"title": title, "body": body, "mains": mains_out})

    return out
