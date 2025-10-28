from django.utils.dateparse import parse_date
from backend.models import RefWebsite
from backend.models import RefBook


def save_websites_from_refs(user, refs):
    """
    อัปเดตเฉพาะ Website (ref_type='1') ลงตาราง RefWebsite
    - 1 row ต่อ 1 รายการ (ref_count) ตามภาษาที่เลือก
    """
    for r in refs:
        if r.get('ref_type') != '1':
            continue
        i      = r.get('ref_count')
        lang   = r.get('language', 'th')
        title  = r.get('title', '')
        url    = r.get('url', '')
        date_s = r.get('access_date', '')
        date_d = parse_date(date_s) if date_s else None
        authors = r.get('authors', [])

        defaults = {
            'ref_web_authors_th': authors if lang == 'th' else [],
            'ref_web_authors_en': authors if lang == 'en' else [],
            'ref_web_title_th'  : title   if lang == 'th' else '',
            'ref_web_title_en'  : title   if lang == 'en' else '',
            'ref_url'           : url,
            'ref_date_access'   : date_d,
        }
        RefWebsite.objects.update_or_create(
            user=user, ref_no=str(i), defaults=defaults
        )


def save_books_from_refs(user, refs):
    """
    ลบของเดิมของ user แล้วบันทึก Book (ref_type='2') ใหม่ทั้งหมด ให้ตรงกับฟอร์มปัจจุบัน
    """
    RefBook.objects.filter(user=user).delete()
    bulk = []

    def _to_int(val):
        try:
            s = (val or '').strip()
            return int(s) if s != '' else None
        except Exception:
            return None

    for r in refs:
        if r.get('ref_type') != '2':
            continue
        lang = r.get('language', 'th')

        kwargs = {'user': user}
        if lang == 'en':
            kwargs.update({
                'book_authors_en'    : r.get('authors', []),
                'book_title_en'      : r.get('title', '') or None,
                'book_print_count_en': _to_int(r.get('print_count')),
                'book_city_print_en' : r.get('city_print', '') or None,
                'book_publisher_en'  : r.get('publisher', '') or None,
                'book_y_print_en'    : _to_int(r.get('y_print')),
            })
        else:
            kwargs.update({
                'book_authors_th'    : r.get('authors', []),
                'book_title_th'      : r.get('title', '') or None,
                'book_print_count_th': _to_int(r.get('print_count')),
                'book_city_print_th' : r.get('city_print', '') or None,
                'book_publisher_th'  : r.get('publisher', '') or None,
                'book_y_print_th'    : _to_int(r.get('y_print')),
            })
        bulk.append(RefBook(**kwargs))

    if bulk:
        RefBook.objects.bulk_create(bulk)
