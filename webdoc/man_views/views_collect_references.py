def collect_references_from_post(request):
    """
    อ่านค่าจากฟอร์มทั้งหมด → list[dict] ตามโครงที่ doc_refer ใช้
    รองรับ ref_type 1..9
    """
    refs = []
    try:
        ref_count = int(request.POST.get('ref_count', 0))
    except (ValueError, TypeError):
        ref_count = 0

    for i in range(1, ref_count + 1):
        ref_type = request.POST.get(f'ref_type_{i}', '')
        lang = request.POST.get(f'lang_{i}', 'th')
        if not ref_type:
            continue

        ref = {'ref_count': i, 'ref_type': ref_type, 'language': lang}

        if ref_type == '1':  # Website
            ref['authors'] = [request.POST.get(f'author_{i}_{j}', '')
                              for j in range(1, 4)
                              if request.POST.get(f'author_{i}_{j}')]
            ref['title']       = request.POST.get(f'title_{i}', '')
            ref['url']         = request.POST.get(f'url_{i}', '')
            ref['access_date'] = request.POST.get(f'access_date_{i}', '')

        elif ref_type == '2':  # Book
            ref['authors']    = [request.POST.get(f'author_{i}_{j}', '')
                                 for j in range(1, 4)
                                 if request.POST.get(f'author_{i}_{j}')]
            ref['title']       = request.POST.get(f'title_{i}', '')
            ref['print_count'] = request.POST.get(f'print_count_{i}', '')
            ref['city_print']  = request.POST.get(f'city_print_{i}', '')
            ref['publisher']   = request.POST.get(f'publisher_{i}', '')
            ref['y_print']     = request.POST.get(f'y_print_{i}', '')

        elif ref_type == '3':  # บทความในหนังสือ
            ref['article_author'] = request.POST.get(f'article_author_{i}', '')
            ref['article_title']  = request.POST.get(f'article_title_{i}', '')
            ref['editor']         = request.POST.get(f'editor_{i}', '')
            ref['book_title']     = request.POST.get(f'book_title_{i}', '')
            ref['city_print']     = request.POST.get(f'city_print_{i}', '')
            ref['publisher']      = request.POST.get(f'publisher_{i}', '')
            ref['y_print']        = request.POST.get(f'y_print_{i}', '')
            ref['pages']          = request.POST.get(f'pages_{i}', '')

        elif ref_type == '4':  # สื่อมัลติมีเดีย
            ref['author']    = request.POST.get(f'author_{i}', '')
            ref['title']     = request.POST.get(f'title_{i}', '')
            ref['format']    = request.POST.get(f'format_{i}', '')
            ref['city_prod'] = request.POST.get(f'city_prod_{i}', '')
            ref['publisher'] = request.POST.get(f'publisher_{i}', '')
            ref['y_prod']    = request.POST.get(f'y_prod_{i}', '')

        elif ref_type == '5':  # หนังสือพิมพ์
            ref['author']         = request.POST.get(f'author_{i}', '')
            ref['article_title']  = request.POST.get(f'article_title_{i}', '')
            ref['newspaper_name'] = request.POST.get(f'newspaper_name_{i}', '')
            ref['pub_date']       = request.POST.get(f'pub_date_{i}', '')
            ref['section']        = request.POST.get(f'section_{i}', '')
            ref['page']           = request.POST.get(f'page_{i}', '')

        elif ref_type == '6':  # บทความในฐานข้อมูล
            ref['author']         = request.POST.get(f'author_{i}', '')
            ref['article_title']  = request.POST.get(f'article_title_{i}', '')
            ref['journal_name']   = request.POST.get(f'journal_name_{i}', '')
            ref['resource_type']  = request.POST.get(f'resource_type_{i}', '')
            ref['db_update_date'] = request.POST.get(f'db_update_date_{i}', '')
            ref['access_date']    = request.POST.get(f'access_date_{i}', '')
            ref['url']            = request.POST.get(f'url_{i}', '')

        elif ref_type == '7':  # Proceedings
            ref['editor']              = request.POST.get(f'editor_{i}', '')
            ref['title']               = request.POST.get(f'title_{i}', '')
            ref['conference_name']     = request.POST.get(f'conference_name_{i}', '')
            ref['conference_date']     = request.POST.get(f'conference_date_{i}', '')
            ref['conference_location'] = request.POST.get(f'conference_location_{i}', '')
            ref['city_print']          = request.POST.get(f'city_print_{i}', '')
            ref['publisher']           = request.POST.get(f'publisher_{i}', '')
            ref['y_print']             = request.POST.get(f'y_print_{i}', '')

        elif ref_type == '8':  # Presentation
            ref['presenter']           = request.POST.get(f'presenter_{i}', '')
            ref['presentation_title']  = request.POST.get(f'presentation_title_{i}', '')
            ref['editor']              = request.POST.get(f'editor_{i}', '')
            ref['conference_name']     = request.POST.get(f'conference_name_{i}', '')
            ref['conference_date']     = request.POST.get(f'conference_date_{i}', '')
            ref['conference_location'] = request.POST.get(f'conference_location_{i}', '')
            ref['city_print']          = request.POST.get(f'city_print_{i}', '')
            ref['publisher']           = request.POST.get(f'publisher_{i}', '')
            ref['y_print']             = request.POST.get(f'y_print_{i}', '')
            ref['page']                = request.POST.get(f'page_{i}', '')

        elif ref_type == '9':  # Journal
            ref['author']        = request.POST.get(f'author_{i}', '')
            ref['article_title'] = request.POST.get(f'article_title_{i}', '')
            ref['journal_name']  = request.POST.get(f'journal_name_{i}', '')
            ref['pub_date']      = request.POST.get(f'pub_date_{i}', '')
            ref['volume_issue']  = request.POST.get(f'volume_issue_{i}', '')
            ref['pages']         = request.POST.get(f'pages_{i}', '')

        refs.append(ref)
    return refs
