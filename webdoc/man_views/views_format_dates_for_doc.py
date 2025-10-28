from .views_format_date_lang import format_date_lang

def format_dates_for_doc(refs):
    """
    แปลงเฉพาะฟิลด์วันที่ที่มาจาก input type='date' ให้เป็นข้อความพร้อมใช้งานใน doc_refer()
    """
    out = []
    for r in refs:
        rt = r.get('ref_type', '')
        lang = r.get('language', 'th')
        r2 = dict(r)
        if rt == '1':  # Website
            r2['access_date'] = format_date_lang(r.get('access_date', ''), lang)
        elif rt == '5':  # Newspaper Article
            r2['pub_date'] = format_date_lang(r.get('pub_date', ''), lang)
        elif rt == '6':  # Database Article
            r2['db_update_date'] = format_date_lang(r.get('db_update_date', ''), lang)
            r2['access_date']    = format_date_lang(r.get('access_date', ''), lang)
        out.append(r2)
    return out
