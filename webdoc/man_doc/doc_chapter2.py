# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any, Dict, List
import json
from docx import Document

# NOTE: ฟังก์ชันอื่น ๆ ด้านล่างนี้สมมติว่ามีอยู่ใน man_doc/doc_function.py เดิมของคุณแล้ว
from man_doc.doc_function import (
    # พื้นฐานเอกสาร
    doc_setup, apply_rest_page_margin,
    # ข้อความทั่วไป
    add_center_paragraph, two_spaces_join, t, as_list,
    # หัวข้อใหญ่ของบท
    add_section_heading_level1_style_1,
    # ย่อหน้าเนื้อหา
    add_body_paragraph_style_1,
    # ย่อหน้าบทนำ/คำอธิบาย
    add_intro_caption_paragraph,
    # รูป + แคปชัน
    add_picture_box_with_caption,
    resolve_image_path,
    # วนต้นไม้หัวข้อย่อย
    walk_item_tree,
    # ==== ฟังก์ชันใหม่ที่เพิ่มใน doc_function.py ====
    make_heading_tap_func_map,
    add_wrapped_paragraph
)

CHAPTER_NO = 2

def parse_intro_for_ch2(intro_body: Any) -> Dict[str, Any]:
    """
    รองรับ intro ทั้งแบบ string และ JSON:
    {"paragraphs":[...], "subnodes":[{"title":"", "paragraphs":[...]}]}
    """
    out = {"paragraphs": [], "subnodes": []}
    if isinstance(intro_body, (dict, list, str)):
        try:
            data = json.loads(intro_body) if isinstance(intro_body, str) else intro_body
            if isinstance(data, dict):
                paras = data.get("paragraphs")
                if isinstance(paras, list):
                    out["paragraphs"] = [
                        t(x if isinstance(x, str) else (x.get("text") if isinstance(x, dict) else ""))
                        for x in paras
                        if t(x if isinstance(x, str) else (x.get("text") if isinstance(x, dict) else ""))
                    ]
                subs = data.get("subnodes")
                if isinstance(subs, list):
                    res = []
                    for sn in subs:
                        if not isinstance(sn, dict):
                            continue
                        res.append({
                            "title": t(sn.get("title")),
                            "paragraphs": [
                                t(x if isinstance(x, str) else (x.get("text") if isinstance(x, dict) else ""))
                                for x in as_list(sn.get("paragraphs"))
                                if t(x if isinstance(x, str) else (x.get("text") if isinstance(x, dict) else ""))
                            ],
                        })
                    out["subnodes"] = res
                return out
        except Exception:
            pass
    s = t(intro_body)
    if s:
        out["paragraphs"] = [p.strip() for p in s.replace("\r\n", "\n").split("\n\n") if p.strip()] or [s]
    return out


def doc_chapter2(
    intro_body: Any = "",
    sections_json: List[Dict[str, Any]] | None = None,
    pictures: List[Dict[str, Any]] | None = None,
    media_root: str = "",
) -> Document:
    sections_json = sections_json or []
    pictures = pictures or []

    # ตั้งค่าหน้ากระดาษ/ฟอนต์มาตรฐาน
    doc = doc_setup()

    # ชื่อบท
    add_center_paragraph(doc, "บทที่ 2", bold=True, font_size=20)
    add_center_paragraph(doc, "เอกสารและงานวิจัยที่เกี่ยวข้อง\n", bold=True, font_size=20)

    # ระยะหน้าถัดไป
    apply_rest_page_margin(doc, top_inch=1.5)

    # -------- สร้าง heading_func ด้วย "map level" ตามสเปค --------
    heading_func = make_heading_tap_func_map(
        level_tap_cm={
            1: 0.00,  # 2.x
            2: 0.75,  # 2.x.x
            3: 2.00,  # 2.x.x.x
            4: 3.40,  # 2.x.x.x.x
            5: 5.10,  # level 5 (ก) ข) ... ) ปรับได้
        },
        level_bold={
            1: True,   
            2: False,  
            3: False,  # level 3 normal
            4: False,  # level 4 normal
            5: False,  # level 5 normal
        },
        alpha_level=5,       # level 5 แสดง ก) ข) ...
        # alpha_list=THAI_ALPHA  # ถ้าต้องการ override
        fallback_left_cm=0.0,
    )

    # -------- บทนำ --------
    intro = parse_intro_for_ch2(intro_body)
    for s in intro.get("paragraphs", []):
        if t(s):
            add_wrapped_paragraph(doc, s, n=99999, custom_tap=0.75,disth=True)

    for i, sn in enumerate(intro.get("subnodes") or []):
        title_no = f"{CHAPTER_NO}.{i + 1}"
        title_txt = t((sn or {}).get("title"))
        if title_no or title_txt:
            add_section_heading_level1_style_1(doc, title_no, title_txt)
        for s in as_list((sn or {}).get("paragraphs")):
            s = t(s)
            if s: add_wrapped_paragraph(doc, s, n=99999, custom_tap=0.75,disth=True)

    # -------- หัวข้อหลัก + ต้นไม้หัวข้อย่อย --------
    pic_counter = [0]   # ใช้ list เพื่ออ้างอิงข้ามฟังก์ชัน
    seen_pics: set[str] = set()

    for sec in sections_json:
        sec_no = t((sec or {}).get("title_no"))
        sec_title = t((sec or {}).get("title"))
        if sec_no or sec_title:
            add_section_heading_level1_style_1(doc, sec_no, sec_title)

        # เนื้อหากล่าวนำของหัวข้อใหญ่
        for raw in as_list((sec or {}).get("body_paragraphs")):
            s = t(raw)
            if s:
                add_body_paragraph_style_1(doc, s)

        # รูปของหัวข้อใหญ่
        for pinfo in as_list((sec or {}).get("pictures")):
            abs_path = resolve_image_path(pinfo, media_root)
            if not abs_path or abs_path in seen_pics:
                continue
            seen_pics.add(abs_path)
            pic_counter[0] += 1
            run_no = pic_counter[0]

            add_picture_box_with_caption(
                doc, abs_path,
                pic_name=t(pinfo.get("pic_name")),
                chapter_no=CHAPTER_NO, run_no=run_no,
            )
            for cap in as_list(pinfo.get("captions")):
                s = t(cap)
                if s:
                    add_intro_caption_paragraph(doc, f"จากภาพที่ {CHAPTER_NO}-{run_no}  {s}")

        # ต้นไม้หัวข้อย่อย (2.1.1+)
        walk_item_tree(
            doc, sec_no, as_list((sec or {}).get("items")),
            media_root=media_root, pic_counter=pic_counter, seen_pics=seen_pics,
            chapter_no=CHAPTER_NO,
            heading_func=heading_func,                 # <<< ใช้ map level ที่ตั้งไว้
            body_func=add_body_paragraph_style_1,
            caption_func=lambda d, s: add_intro_caption_paragraph(
                d, f"จากภาพที่ {CHAPTER_NO}-{pic_counter[0]}  {t(s)}"
            ),
        )


    return doc

# aliases
doc_chapter_2 = doc_chapter2
generate_doc = doc_chapter2
