# man_doc/doc_chapter2.py
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from django.conf import settings
import os

# ⬇️ ดึงจาก doc_function.py ที่มีอยู่แล้ว
from man_doc.doc_function import doc_setup, iter_sections, sections_doc_safe, _t

FONT = "TH SarabunPSK"
BASE_PT = 16
TITLE_PT = 20

def addCaption(doc, chap_no, pic_no, pic_name):
    cap = doc.add_paragraph()
    run = cap.add_run(f"ภาพที่ {chap_no}-{pic_no} {pic_name or ''}")
    run.bold = True
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

def generateDocxChapter2(user, chap, doc, pictures):
    d = doc_setup()  # ✅ ใช้ฟังก์ชันกลางของคุณ

    # ชื่อบท
    h = d.add_paragraph()
    r = h.add_run(f"บทที่ {chap.chap_no} เอกสารและงานวิจัยที่เกี่ยวข้อง")
    r.bold = True
    r.font.size = Pt(TITLE_PT)

    # ย่อหน้าเกริ่น
    if doc and (doc.intro_body or "").strip():
        p = d.add_paragraph(doc.intro_body.strip())
        p.paragraph_format.first_line_indent = Inches(0.5)

    # ส่วนหัวข้อย่อย: ใช้ iterator กลาง
    sections_any = getattr(doc, 'sections_json', '[]')
    for title, body, mains in iter_sections(sections_any, first_section_mode="body"):
        if _t(title):
            t = d.add_paragraph(_t(title))
            if t.runs:
                t.runs[0].bold = True
        if _t(body):
            pb = d.add_paragraph(_t(body))
            pb.paragraph_format.first_line_indent = Inches(0.5)
        # ถ้าในอนาคตต้องเรนเดอร์ mains/subs ก็วนต่อที่นี่ได้

    # รวมรูปภาพทั้งหมด เรียงตาม pic_no (อ่านจาก JSON)
    pic_items = []
    for p in pictures:
        data = p.get_data()
        try:
            pic_items.append({
                "no": int(data.get("pic_no") or 0),
                "name": data.get("pic_name") or "",
                "path": data.get("pic_path") or "",
            })
        except Exception:
            pass
    pic_items.sort(key=lambda x: x["no"])

    for item in pic_items:
        abs_path = os.path.join(settings.MEDIA_ROOT, item["path"])
        if os.path.exists(abs_path):
            try:
                d.add_picture(abs_path, width=Inches(5.5))
            except Exception:
                pass
        addCaption(d, chap.chap_no, item["no"], item["name"])

    out_dir = os.path.join("media", "exports", f"user_{user.id}")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"chapter2_user{user.id}_chap{chap.chap_no}.docx")
    d.save(out_path)
    return "/" + out_path.replace("\\", "/")
