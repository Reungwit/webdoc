from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import os
from django.http import HttpResponse

def doc_refer(references):
    doc = Document()
    # ตั้งค่า Style เริ่มต้น
    style = doc.styles["Normal"]
    style.font.name = "TH SarabunPSK"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "TH SarabunPSK")
    style.font.size = Pt(16)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0
    
    # ตั้งค่าขอบกระดาษ
    section = doc.sections[0]
    section.top_margin = Inches(1.5)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1)

    # เพิ่มหัวข้อ "เอกสารอ้างอิง"
    heading = doc.add_paragraph('บรรณานุกรม')
    # heading.style.font.bold = True
    heading.alignment = 1 # 1 

    for ref in references:
        ref_type = ref.get('ref_type')
        ref_count = ref.get('ref_count', '')
        
        # สร้าง paragraph สำหรับแต่ละ reference
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(-0.5) # Hanging indent
        p.paragraph_format.left_indent = Inches(0.5)

        # สร้างข้อความอ้างอิง
        text = ''

        if ref_type == '1': # 1. เว็บไซต์
            author = ref.get('author', 'N.p.')
            title = ref.get('title', 'N.t.')
            url = ref.get('url', '')
            access_date = ref.get('access_date', '')
            text = f'{author}. {title}. Available at: URL:{url}. Accessed {access_date}.'
        
        elif ref_type == '2': # 2. หนังสือ
            author = ref.get('author', '')
            title = ref.get('title', '')
            print_count = ref.get('print_count', '')
            city_print = ref.get('city_print', '')
            publisher = ref.get('publisher', '')
            y_print = ref.get('y_print', '')
            edition_text = f'{print_count} ed. ' if print_count else ''
            text = f'{author}. {title}. {edition_text}{city_print}:{publisher};{y_print}.'

        elif ref_type == '3': # 3. บทความในหนังสือ
            article_author = ref.get('article_author', '')
            article_title = ref.get('article_title', '')
            editor = ref.get('editor', '')
            book_title = ref.get('book_title', '')
            city_print = ref.get('city_print', '')
            publisher = ref.get('publisher', '')
            y_print = ref.get('y_print', '')
            pages = ref.get('pages', '')
            text = f'{article_author}. {article_title}. In: {editor}, editor. {book_title}. {city_print}: {publisher}; {y_print}. p. {pages}.'

        elif ref_type == '4': # 4. สื่อมัลติมีเดีย
            author = ref.get('author', '')
            title = ref.get('title', '')
            format_type = ref.get('format', '')
            city_prod = ref.get('city_prod', '')
            publisher = ref.get('publisher', '')
            y_prod = ref.get('y_prod', '')
            text = f'{author}. {title} [{format_type}]. {city_prod}: {publisher}; {y_prod}.'

        elif ref_type == '5': # 5. บทความจากหนังสือพิมพ์
            author = ref.get('author', '')
            article_title = ref.get('article_title', '')
            newspaper_name = ref.get('newspaper_name', '')
            pub_date = ref.get('pub_date', '')
            section = ref.get('section', '')
            page = ref.get('page', '')
            text = f'{author}. {article_title}. {newspaper_name} {pub_date};{section}:{page}.'

        elif ref_type == '6': # 6. บทความในฐานข้อมูล
            author = ref.get('author', '')
            article_title = ref.get('article_title', '')
            journal_name = ref.get('journal_name', '')
            resource_type = ref.get('resource_type', '[serial online]')
            db_update_date = ref.get('db_update_date', '')
            access_date = ref.get('access_date', '')
            pages = ref.get('pages', '')
            url = ref.get('url', '')
            text = f'{author}. {article_title}. {journal_name} [{resource_type}] [updated {db_update_date}; cited {access_date}]. Available from: {url}'

        elif ref_type == '7': # 7. รายงานการประชุม
            editor = ref.get('editor', '')
            title = ref.get('title', '')
            conf_name = ref.get('conference_name', '')
            conf_date = ref.get('conference_date', '')
            conf_loc = ref.get('conference_location', '')
            city_print = ref.get('city_print', '')
            publisher = ref.get('publisher', '')
            y_print = ref.get('y_print', '')
            text = f'{editor}, editor. {title}. Proceedings of the {conf_name}; {conf_date}; {conf_loc}. {city_print}: {publisher}; {y_print}.'

        elif ref_type == '8': # 8. การนำเสนอผลงานในการประชุม
            presenter = ref.get('presenter', '')
            pres_title = ref.get('presentation_title', '')
            editor = ref.get('editor', '')
            conf_name = ref.get('conference_name', '')
            conf_date = ref.get('conference_date', '')
            conf_loc = ref.get('conference_location', '')
            city_print = ref.get('city_print', '')
            publisher = ref.get('publisher', '')
            y_print = ref.get('y_print', '')
            page = ref.get('page', '')
            text = f'{presenter}. {pres_title}. In: {editor}, editor. {conf_name}; {conf_date}; {conf_loc}. {city_print}: {publisher}; {y_print}. p. {page}.'

        elif ref_type == '9': # 9. บทความในวารสาร
            author = ref.get('author', '')
            article_title = ref.get('article_title', '')
            journal_name = ref.get('journal_name', '')
            pub_date = ref.get('pub_date', '')
            vol_issue = ref.get('volume_issue', '')
            pages = ref.get('pages', '')
            text = f'{author}. {article_title}. {journal_name} {pub_date};{vol_issue}:{pages}.'

        if text:
            # เพิ่มหมายเลขอ้างอิงและเนื้อหาลงใน paragraph
            p.add_run(f'[{ref_count}] ')
            p.add_run(text)

    return doc