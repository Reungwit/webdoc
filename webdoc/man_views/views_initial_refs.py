from backend.models import RefWebsite
from backend.models import RefBook

def initial_refs_web_from_db(user):
    """
    ดึง Website ของ user → สร้าง list[dict] สำหรับ hydrate ฟอร์ม refer.html
    """
    rows = RefWebsite.objects.filter(user=user).order_by('ref_no', 'ref_web_id')
    out = []
    for r in rows:
        lang = 'en' if (r.ref_web_title_en or r.ref_web_authors_en) else 'th'
        authors = r.ref_web_authors_en if lang == 'en' else r.ref_web_authors_th
        title   = r.ref_web_title_en   if lang == 'en' else r.ref_web_title_th
        out.append({
            'ref_type'   : '1',
            'language'   : lang,
            'authors'    : authors or [],
            'title'      : title or '',
            'url'        : r.ref_url or '',
            'access_date': r.ref_date_access.isoformat() if r.ref_date_access else '',
        })
    return out

def initial_books_from_db(user):
    """
    ดึง Book ของ user → คืนเป็นรายการสำหรับ hydrate ฟอร์ม refer.html
    """
    out = []
    for b in RefBook.objects.filter(user=user).order_by('ref_book_id'):
        # TH
        if (b.book_title_th or b.book_authors_th or b.book_city_print_th
            or b.book_publisher_th or b.book_y_print_th is not None
            or b.book_print_count_th is not None):
            out.append({
                'ref_type'   : '2',
                'language'   : 'th',
                'authors'    : b.book_authors_th or [],
                'title'      : b.book_title_th or '',
                'print_count': b.book_print_count_th if b.book_print_count_th is not None else '',
                'city_print' : b.book_city_print_th or '',
                'publisher'  : b.book_publisher_th or '',
                'y_print'    : b.book_y_print_th if b.book_y_print_th is not None else '',
            })
        # EN
        if (b.book_title_en or b.book_authors_en or b.book_city_print_en
            or b.book_publisher_en or b.book_y_print_en is not None
            or b.book_print_count_en is not None):
            out.append({
                'ref_type'   : '2',
                'language'   : 'en',
                'authors'    : b.book_authors_en or [],
                'title'      : b.book_title_en or '',
                'print_count': b.book_print_count_en if b.book_print_count_en is not None else '',
                'city_print' : b.book_city_print_en or '',
                'publisher'  : b.book_publisher_en or '',
                'y_print'    : b.book_y_print_en if b.book_y_print_en is not None else '',
            })
    return out
