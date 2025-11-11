# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any, Dict, List

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt
from docx.oxml.ns import qn

from man_doc.doc_function import (
    doc_setup,
    apply_rest_page_margin,
    add_center_paragraph,
    add_body_paragraph_style_1,
    add_section_heading_level1_style_1,
    add_section_heading_level2_plus_style_1,
    add_picture_box_with_caption,
    walk_item_tree,
    resolve_image_path,
    t, as_list,
)

CHAPTER_NO = 3   # เลขบทสำหรับรันเลขรูป: ภาพที่ 3-1, 3-2, ...

def add_tables_from_json(doc: Document, tables_json, font_name="TH SarabunPSK", base_pt=16):
    """วาดตารางจากโครงสร้าง [{caption, headers, rows, ...}]"""
    if not tables_json:
        return
    for tinfo in tables_json:
        headers = tinfo.get("headers") or []
        rows = tinfo.get("rows") or []
        caption = tinfo.get("caption") or ""
        ncols = len(headers) or (len(rows[0]) if rows else 0)
        ncols = max(1, ncols)

        # คำอธิบายตาราง (caption)
        if caption:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(caption)
            run.bold = True
            run.font.name = font_name
            run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
            run.font.size = Pt(base_pt)

        # ตาราง
        table = doc.add_table(rows=len(rows)+1, cols=ncols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.style = 'Table Grid'

        # ส่วนหัว
        for ci in range(ncols):
            text = headers[ci] if ci < len(headers) else f"หัว {ci+1}"
            cell = table.cell(0, ci)
            cell.text = str(text)
            for run in cell.paragraphs[0].runs:
                run.font.bold = True
                run.font.name = font_name
                run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
                run.font.size = Pt(base_pt)

        # เนื้อหาตาราง
        for ri, row in enumerate(rows, start=1):
            for ci in range(ncols):
                v = row[ci] if ci < len(row) else ""
                cell = table.cell(ri, ci)
                cell.text = str(v)
                for run in cell.paragraphs[0].runs:
                    run.font.name = font_name
                    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
                    run.font.size = Pt(base_pt)

        # เว้นวรรคหลังตาราง
        doc.add_paragraph("")


def _render_intro(doc: Document, intro_any: Any) -> None:
    """
    intro_any รองรับ:
      - str  : ย่อหน้าเดียว
      - dict : {"paragraphs": [...], "items": [...], "pictures":[...]}
    """
    if isinstance(intro_any, dict):
        for raw in as_list(intro_any.get("paragraphs")):
            s = t(raw)
            if s:
                add_body_paragraph_style_1(doc, s)

        # วาดรูปจากบทนำ
        pic_counter = [0]
        seen_pics: set[str] = set()
        for pinfo in as_list(intro_any.get("pictures")):
            abs_path = resolve_image_path(pinfo, "")
            if not abs_path or abs_path in seen_pics:
                continue
            seen_pics.add(abs_path)
            pic_counter[0] += 1
            add_picture_box_with_caption(
                doc,
                abs_path,
                pic_name=t((pinfo or {}).get("pic_name")),
                chapter_no=CHAPTER_NO,
                run_no=pic_counter[0],
            )

        # items ใต้บทนำ (เลือกใช้หรือไม่ก็ได้)
        items = as_list(intro_any.get("items"))
        if items:
            walk_item_tree(
                doc,
                section_no="",
                nodes=items,
                chapter_no=CHAPTER_NO,
                media_root="",
                pic_counter=pic_counter,
                seen_pics=seen_pics,
                heading_func=add_section_heading_level2_plus_style_1,
                body_func=add_body_paragraph_style_1,
            )
        return

    s = t(intro_any)
    if s:
        add_body_paragraph_style_1(doc, s)


def _render_sections(doc: Document, sections_json: List[Dict[str, Any]] | None, *, media_root: str = "") -> None:
    sections_json = sections_json or []
    pic_counter = [0]
    seen_pics: set[str] = set()

    for sec in sections_json:
        sec_no    = t((sec or {}).get("title_no"))
        sec_title = t((sec or {}).get("title"))

        # หัวข้อระดับ 1
        if sec_no or sec_title:
            add_section_heading_level1_style_1(doc, sec_no, sec_title)

        # เนื้อหาใต้หัวข้อ
        for raw in as_list((sec or {}).get("body_paragraphs")):
            s = t(raw)
            if s:
                add_body_paragraph_style_1(doc, s)

        # รูประดับหัวข้อ
        for pinfo in as_list((sec or {}).get("pictures")):
            abs_path = resolve_image_path(pinfo, media_root)
            if not abs_path or abs_path in seen_pics:
                continue
            seen_pics.add(abs_path)
            pic_counter[0] += 1
            add_picture_box_with_caption(
                doc,
                abs_path,
                pic_name=t((pinfo or {}).get("pic_name")),
                chapter_no=CHAPTER_NO,
                run_no=pic_counter[0],
            )

        # หัวข้อย่อยเป็นต้นไม้
        walk_item_tree(
            doc,
            sec_no,
            as_list((sec or {}).get("items")),
            chapter_no=CHAPTER_NO,
            media_root=media_root,
            pic_counter=pic_counter,
            seen_pics=seen_pics,
            heading_func=add_section_heading_level2_plus_style_1,
            body_func=add_body_paragraph_style_1,
        )


def doc_chapter3(
    intro_body: Any = "",
    sections_json: List[Dict[str, Any]] | None = None,
    tables_json: List[Dict[str, Any]] | None = None,
    media_root: str = "",
) -> Document:
    """
    ตัวสร้างไฟล์บทที่ 3
    - intro_body  : str หรือ dict {"paragraphs":[...], "items":[...], "pictures":[...]}
    - sections_json: โครงสร้างหัวข้อ/ย่อหน้าย่อย
    - tables_json : [{caption, headers, rows, ...}]
    """
    doc = doc_setup()

    # หัวบท
    add_center_paragraph(doc, "บทที่ 3", bold=True, font_size=20)
    add_center_paragraph(doc, "ระเบียบวิธีวิจัย", bold=True, font_size=20)

    # ปรับ margin หน้าถัดไป
    apply_rest_page_margin(doc, top_inch=1.5)

    # บทนำ
    _render_intro(doc, intro_body)

    # หัวข้อใหญ่/ย่อย
    _render_sections(doc, sections_json or [], media_root=media_root)

    # ตาราง
    add_tables_from_json(doc, tables_json)

    return doc

# aliases
doc_chapter_3 = doc_chapter3
generate_doc = doc_chapter3
