def current_user_id(request):
    """
    คืน user_id ของผู้ใช้ปัจจุบันแบบปลอดภัย: ใช้ user.user_id > user.id > POST[user_id]
    """
    uid = getattr(request.user, 'user_id', None) or getattr(request.user, 'id', None)
    if not uid:
        try:
            uid = int((request.POST.get('user_id') or '').strip())
        except Exception:
            uid = None
    return uid
