# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any, Dict, List
import json
from docx import Document

from man_doc.doc_function import (
    doc_setup, apply_rest_page_margin,
    add_center_paragraph, two_spaces_join,
    add_section_heading_level1_style_1, add_section_heading_level2_plus_style_1,
    add_body_paragraph_style_1,            # ย่อหน้าเนื้อหา (ทั่วไป)
    add_intro_caption_paragraph,           # ย่อหน้าบทนำ/คำอธิบายใต้รูป (เฉพาะ)
    add_picture_box_with_caption,
    walk_item_tree, resolve_image_path, t, as_list,
)

CHAPTER_NO = 2

def _parse_intro(intro_body: Any) -> Dict[str, Any]:
    """
    รองรับได้ทั้ง string เดิม และ JSON:
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
                        for x in paras if t(x if isinstance(x, str) else (x.get("text") if isinstance(x, dict) else ""))
                    ]
                subs = data.get("subnodes")
                if isinstance(subs, list):
                    res = []
                    for sn in subs:
                        if not isinstance(sn, dict): continue
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
        out["paragraphs"] = [p.strip() for p in s.replace("\r\n","\n").split("\n\n") if p.strip()] or [s]
    return out

def doc_chapter2(
    intro_body: Any = "",
    sections_json: List[Dict[str, Any]] | None = None,
    pictures: List[Dict[str, Any]] | None = None,
    media_root: str = "",
) -> Document:
    """
    - บทนำ/หัวข้อย่อยบทนำ/คำอธิบายใต้รูป → add_intro_caption_paragraph (indent 1.25 ซม.)
    - เนื้อหา (2.1.1 ฯลฯ) → add_body_paragraph_style_1 (indent 1.80 ซม.)
    - คำอธิบายใต้รูป มีข้อความตายตัว: "จากภาพที่ <บท>-<เลขภาพ>  <ข้อความผู้ใช้>"
    """
    sections_json = sections_json or []
    pictures = pictures or []

    doc = doc_setup()

    # หัวบท
    add_center_paragraph(doc, "บทที่ 2", bold=True, font_size=20)
    add_center_paragraph(doc, "เอกสารและงานวิจัยที่เกี่ยวข้อง", bold=True, font_size=20)

    apply_rest_page_margin(doc, top_inch=1.5)

    # -------- 1) บทนำ --------
    intro = _parse_intro(intro_body)
    for s in intro.get("paragraphs", []):
        if t(s): add_intro_caption_paragraph(doc, s)

    for i, sn in enumerate(intro.get("subnodes") or []):
        title_no = f"{CHAPTER_NO}.{i+1}"
        title_txt = t((sn or {}).get("title"))
        if title_no or title_txt:
            add_section_heading_level1_style_1(doc, title_no, title_txt)
        for s in as_list((sn or {}).get("paragraphs")):
            s = t(s)
            if s: add_intro_caption_paragraph(doc, s)

    # -------- 2) หัวข้อหลัก --------
    pic_counter = [0]   # ใช้ list เพื่อให้ส่งอ้างอิงเข้า walk_item_tree ได้
    seen_pics: set[str] = set()

    for sec in sections_json:
        sec_no = t((sec or {}).get("title_no"))
        sec_title = t((sec or {}).get("title"))
        if sec_no or sec_title:
            add_section_heading_level1_style_1(doc, sec_no, sec_title)

        # เนื้อหากล่าวนำของหัวข้อใหญ่
        for raw in as_list((sec or {}).get("body_paragraphs")):
            s = t(raw)
            if s: add_body_paragraph_style_1(doc, s)

        # รูปของหัวข้อใหญ่ + แคปชันแบบ "จากภาพที่ 2-x  <caption>"
        for pinfo in as_list((sec or {}).get("pictures")):
            abs_path = resolve_image_path(pinfo, media_root)
            if not abs_path or abs_path in seen_pics: continue
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
                    # 1 วรรคหลัง "จากภาพที่", 2 วรรคก่อนข้อความผู้ใช้
                    add_intro_caption_paragraph(doc, f"จากภาพที่ {CHAPTER_NO}-{run_no}  {s}")

        # หัวข้อย่อยแบบ tree (2.1.1+)
        # ส่ง caption_func ที่อิงค่าปัจจุบันของ pic_counter[0]
        walk_item_tree(
            doc, sec_no, as_list((sec or {}).get("items")),
            media_root=media_root, pic_counter=pic_counter, seen_pics=seen_pics,
            chapter_no=CHAPTER_NO,
            heading_func=add_section_heading_level2_plus_style_1,
            body_func=add_body_paragraph_style_1,
            caption_func=lambda d, s: add_intro_caption_paragraph(
                d, f"จากภาพที่ {CHAPTER_NO}-{pic_counter[0]}  {t(s)}"
            ),
        )

    # -------- 3) รูปท้ายบท (ถ้ามี) --------
    if pictures:
        for pinfo in pictures:
            abs_path = resolve_image_path(pinfo, media_root)
            if not abs_path or abs_path in seen_pics: continue
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

    return doc

# aliases
doc_chapter_2 = doc_chapter2
generate_doc = doc_chapter2