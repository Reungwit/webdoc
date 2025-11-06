# -*- coding: utf-8 -*-
"""
doc_chapter2.py — บทที่ 2 (ฉบับเต็ม)
(แก้ไขให้เรียกใช้ฟังก์ชันกลางจาก doc_function.py)
"""

from __future__ import annotations
import os
from typing import Any, Dict, List

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Import ทุกอย่างจากไฟล์กลาง
from man_doc.doc_function import *
    
# CHAPTER_NO ยังคงจำเป็นต้องมีในไฟล์นี้ เพื่อส่งค่า "2" 
# เข้าไปในฟังก์ชันกลาง
CHAPTER_NO = 2  

# ===================== main =====================

def doc_chapter2(
    intro_body: str = "",
    sections_json: List[Dict[str, Any]] | None = None,
    pictures: List[Dict[str, Any]] | None = None,
    media_root: str = "",
) -> Document:
    """
    ตัวสร้างไฟล์บทที่ 2 (ปรับปรุงตาม requirement ใหม่)
    (เรียกใช้ฟังก์ชันกลางทั้งหมด)
    """
    sections_json = sections_json or []
    pictures = pictures or []

    doc = doc_setup()

    # หัวบท
    add_center_paragraph(doc, "บทที่ 2", bold=True, font_size=20)
    add_center_paragraph(doc, "เอกสารและงานวิจัยที่เกี่ยวข้อง", bold=True, font_size=20)

    apply_rest_page_margin(doc, top_inch=1.5)

    # ย่อหน้าเปิดบท (โหมด paragraphs)
    if t(intro_body):
        # (แก้ไข) เรียกใช้ฟังก์ชันสไตล์ที่กำหนดไว้ในไฟล์กลาง
        add_body_paragraph_style_1(doc, t(intro_body))

    pic_counter = [0]
    seen_pics: set[str] = set()

    # หัวข้อหลักทั้งบท
    for sec in sections_json:
        sec_no = t((sec or {}).get("title_no"))
        sec_title = t((sec or {}).get("title"))
        if sec_no or sec_title:
            # (แก้ไข) เรียกใช้ฟังก์ชันสไตล์ที่กำหนดไว้ในไฟล์กลาง
            add_section_heading_level1_style_1(doc, sec_no, sec_title)

        # เนื้อหาใต้หัวข้อหลัก (ขึ้นบรรทัดใหม่ตามปกติ)
        for raw in as_list((sec or {}).get("body_paragraphs")):
            s = t(raw)
            if s:
                # (แก้ไข) เรียกใช้ฟังก์ชันสไตล์ที่กำหนดไว้ในไฟล์กลาง
                add_body_paragraph_style_1(doc, s) 

        # รูประดับหัวข้อ (ถ้ามี)
        for pinfo in as_list((sec or {}).get("pictures")):
            abs_path = resolve_image_path(pinfo, media_root)
            if not abs_path or abs_path in seen_pics:
                continue
            seen_pics.add(abs_path)
            pic_counter[0] += 1
            
            # (แก้ไข) ส่ง chapter_no เข้าไปในฟังก์ชันกลาง
            add_picture_box_with_caption(
                doc,
                abs_path,
                pic_name=t(pinfo.get("pic_name")),
                chapter_no=CHAPTER_NO, # <-- ส่งเลขบท
                run_no=pic_counter[0],
            )

        # หัวข้อย่อยแบบต้นไม้ (2.1.1+ → ปรับปรุงแล้ว)
        walk_item_tree(
            doc,
            sec_no,
            as_list((sec or {}).get("items")),
            media_root=media_root,
            pic_counter=pic_counter,
            seen_pics=seen_pics,
            
            # (แก้ไข) ส่ง chapter_no และฟังก์ชันสไตล์เข้าไป
            chapter_no=CHAPTER_NO,
            heading_func=add_section_heading_level2_plus_style_1,
            body_func=add_body_paragraph_style_1
        )

    # รูปท้ายบท (ถ้าส่งมา)
    if pictures:
        doc.add_paragraph().add_run().add_break()
        for pinfo in pictures:
            abs_path = resolve_image_path(pinfo, media_root)
            if not abs_path or abs_path in seen_pics:
                continue
            seen_pics.add(abs_path)
            pic_counter[0] += 1
            
            # (แก้ไข) ส่ง chapter_no เข้าไปในฟังก์ชันกลาง
            add_picture_box_with_caption(
                doc,
                abs_path,
                pic_name=t(pinfo.get("pic_name")),
                chapter_no=CHAPTER_NO, # <-- ส่งเลขบท
                run_no=pic_counter[0],
            )

    return doc

# aliases
doc_chapter_2 = doc_chapter2
generate_doc = doc_chapter2