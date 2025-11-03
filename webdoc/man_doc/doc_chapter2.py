# -*- coding: utf-8 -*-
"""
ตัวสร้างไฟล์ .docx สำหรับบทที่ 2
- intro_body: str
- sections_json: list
- pictures: [{"pic_name": str, "pic_path": "img/user_<username>/xxx.png"}, ...]
- media_root: absolute path ของ MEDIA_ROOT
"""
import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


def _p(doc, text="", bold=False, size=12, align=None, before=4, after=6):
    para = doc.add_paragraph()
    if align is not None:
        para.alignment = align
    run = para.add_run(text or "")
    run.bold = bold
    run.font.size = Pt(size)
    pf = para.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    return para


def _walk_nodes(doc, section_no, nodes):
    if not isinstance(nodes, list):
        return
    for i, node in enumerate(nodes):
        node_no = f"{section_no}.{i+1}"
        title = (node or {}).get("text") or ""
        if title:
            _p(doc, f"{node_no} {title}", bold=True, size=13, before=8, after=4)
        for para in (node or {}).get("paragraphs", []) or []:
            _p(doc, para or "", size=12, before=0, after=6)
        _walk_nodes(doc, node_no, (node or {}).get("children", []) or [])


def doc_chapter2(intro_body="", sections_json=None, pictures=None, media_root=""):
    sections_json = sections_json or []
    pictures = pictures or []

    doc = Document()
    _p(doc, "บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง", bold=True, size=18, before=0, after=12)

    if intro_body:
        _p(doc, intro_body, size=12, before=0, after=10)

    for sec in sections_json:
        sec_no = (sec or {}).get("title_no") or ""
        sec_title = (sec or {}).get("title") or ""
        if sec_no:
            _p(doc, f"{sec_no} {sec_title}".strip(), bold=True, size=14, before=10, after=6)
        for para in (sec or {}).get("body_paragraphs", []) or []:
            _p(doc, para or "", size=12, before=0, after=6)
        _walk_nodes(doc, sec_no, (sec or {}).get("items", []) or [])

    # รูปภาพท้ายบท
    if pictures:
        _p(doc, "", size=12, before=6, after=0)
        running = 1
        for p in pictures:
            name = (p or {}).get("pic_name") or ""
            rel = ((p or {}).get("pic_path") or "").replace("\\", "/")
            abs_path = os.path.join(media_root or "", rel).replace("\\", os.sep)
            if not os.path.isfile(abs_path):
                # ถ้าไฟล์ไม่มีจริง ข้าม
                continue

            # image
            par = doc.add_paragraph()
            par.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            run = par.add_run()
            run.add_picture(abs_path, width=Inches(5))
            par.paragraph_format.space_after = Pt(8)

            running += 1
            
            # caption
            _p(
                doc,
                f"ภาพที่ 2-{running} {name}",
                size=12,
                align=WD_PARAGRAPH_ALIGNMENT.CENTER,
                before=6,
                after=4,
            )
            

    return doc


# alias
doc_chapter_2 = doc_chapter2
generate_doc = doc_chapter2
