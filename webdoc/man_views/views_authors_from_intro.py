import json

def authors_from_intro(intro):
    """
    ดึงชื่อผู้จัดทำจาก intro.student_name (JSON/dict: {"th":[...], "en":[...]})
    คืนค่า: author1_th, author2_th, author1_en, author2_en (อาจเป็น string ว่าง)
    """
    data = getattr(intro, 'student_name', None) or {}
    th, en = [], []
    try:
        if isinstance(data, dict):
            th = data.get('th') or []
            en = data.get('en') or []
        else:
            parsed = json.loads(data)
            if isinstance(parsed, dict):
                th = parsed.get('th', []) or []
                en = parsed.get('en', []) or []
    except Exception:
        th, en = [], []

    th = [(th[i] or '').strip() if i < len(th) else '' for i in range(2)]
    en = [(en[i] or '').strip() if i < len(en) else '' for i in range(2)]
    return th[0], th[1], en[0], en[1]
