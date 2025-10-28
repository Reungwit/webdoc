from django.utils.dateparse import parse_date

def format_date_lang(date_s: str, lang: str) -> str:
    """
    รับ 'YYYY-MM-DD' → คืนสตริงตามภาษา: en='YYYY Mon DD', th='DD Mon YYYY(พ.ศ.)'
    """
    if not date_s:
        return ''
    d = parse_date(date_s)
    if not d:
        return ''
    months_th = ["ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.","ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."]
    months_en = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    if lang == 'en':
        return f"{d.year} {months_en[d.month-1]} {d.day}"
    year_th = d.year + 543
    return f"{d.day} {months_th[d.month-1]} {year_th}"
