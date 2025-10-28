def is_intro_ok_check(intro) -> bool:
    """
    เช็คข้อมูล Project Setup ครบขั้นต่ำ:
    - มีชื่อโครงงาน TH/EN
    - มีผู้จัดทำ (TH หรือ EN อย่างน้อย 1)
    """
    if not intro:
        return False
    if not getattr(intro, 'name_pro_th', None) or not getattr(intro, 'name_pro_en', None):
        return False
    data = getattr(intro, 'student_name', None) or {}
    names_th = data.get('th', []) if isinstance(data, dict) else []
    names_en = data.get('en', []) if isinstance(data, dict) else []
    return bool(names_th or names_en)
