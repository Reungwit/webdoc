# backend/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db import transaction, IntegrityError
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage

import json
import re
import copy
import traceback
from io import BytesIO

# Forms / Models
from .forms import RegisterForm, LoginForm
from .models import (
    SpProject, SpProjectAuthor, DocCover, Certificate, Chapter1, RefWebsite, RefBook,
    Chapter5, DocIntroduction, DocAbstract, DocChapter3
)

# DOCX builders
from man_doc.doc_sp_01 import doc_sp_01
from man_doc.doc_cover import doc_cover_th, doc_cover_en, doc_cover_sec
from man_doc.doc_abstract_ack import doc_abstract_ack
from man_doc.doc_refer import doc_refer
from man_doc.doc_chapter5 import doc_chapter5
from man_doc.doc_chapter1 import doc_chapter1
from man_doc.doc_certificate import doc_certificate
# ---------- บทที่ 3: ตัวสร้างเอกสาร (ให้คุณมีไฟล์ man_doc/doc_chapter3.py ชื่อฟังก์ชัน generate_doc) ----------
# signature แนะนำ: generate_doc(intro_body, sections_json, tables_json, pictures, media_root)
try:
    from man_doc.doc_chapter3 import generate_doc as generate_doc_ch3
except Exception:
    generate_doc_ch3 = None

# ====== imports from man_views (helpers ที่แยกออก) ======
from man_views.views_current_user_id import current_user_id as current_user_id
from man_views.views_is_intro_ok_check import is_intro_ok_check
from man_views.views_authors_from_intro import authors_from_intro as _authors_from_intro

# รวม helper อ้างอิง (ตามไฟล์ที่คุณรวม)
from man_views.views_save_refs import save_websites_from_refs, save_books_from_refs
from man_views.views_initial_refs import initial_refs_web_from_db, initial_books_from_db

from man_views.views_format_dates_for_doc import format_dates_for_doc
from man_views.views_collect_references import collect_references_from_post

# ---------------- บทที่ 1 ----------------
from man_views.views_chapter_1 import chapter_1_view as chapter_1_view_logic

# ---------------- บทที่ 2  ----------------
from man_views.views_chapter_2 import chapter_2_view as chapter_2_view_logic

# ---------------- บทที่ 5  ----------------
from man_views.views_chapter_5 import chapter_5_view as chapter_5_view_logic
# ========================================================


# ---------------- Basic pages ----------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    user = request.user
    intro = DocIntroduction.objects.filter(user=user).first()
    if not intro or not is_intro_ok_check(intro):
        messages.info(request, 'โปรดกรอกข้อมูลเบื้องต้นของโครงงานก่อนเข้าใช้งานในส่วนอื่นๆ')
        return redirect('project_setup')
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'index.html')

def sp_project_form_view(request):
    return render(request, 'sp_project_form.html')

def intro_view(request):
    return render(request, 'intro.html')

def chapter_1_view(request):
    return chapter_1_view_logic(request)

def chapter_2_view(request):
    return chapter_2_view_logic(request)


# ========= บทที่ 3 =========
def safe_parse_list(raw_text, fallback):
    """
    แปลง string JSON -> list อย่างปลอดภัย (ใช้สำหรับบทที่ 3)
    """
    try:
        data = json.loads(raw_text or '[]')
        return data if isinstance(data, list) else (fallback or [])
    except json.JSONDecodeError:
        return fallback or []

@login_required
def chapter_3_view(request):
    user = request.user

    # 0) เคลียร์ message ที่ยังค้างมาจากหน้าก่อน (เช่น บทที่ 5)
    for _ in messages.get_messages(request):
        pass  # consume แล้วเคลียร์

    # ดึงข้อมูลล่าสุดของ user
    row = DocChapter3.objects.filter(user=user).order_by('-updated_at').first()
    db_intro   = (getattr(row, "intro_body", "") or "")
    db_secs    = row.sections_json if (row and isinstance(row.sections_json, list)) else []
    db_tables  = row.tb_sections_json if (row and isinstance(row.tb_sections_json, list)) else []

    if request.method == 'GET':
        return render(request, 'chapter_3.html', {
            'page_title': 'บทที่ 3 วิธีดำเนินการ/การออกแบบ/ผลลัพธ์',
            'initial': {
                'intro_body': db_intro,
                'sections': db_secs,
                'tables': db_tables,
                'chapter3_json': db_secs,
                'chapter3_tables_json': db_tables,
            }
        })

    action = (request.POST.get('action') or '').strip()
    intro_body = (request.POST.get('intro_body') or '').strip()
    raw_secs   = request.POST.get('sections_json', None)
    if raw_secs is None:
        raw_secs = request.POST.get('chapter3_json', '')
    raw_tables = request.POST.get('tables_json', None)
    if raw_tables is None:
        raw_tables = request.POST.get('chapter3_tables_json', '')

    if action == 'add_picture':
        try:
            pic_name = (request.POST.get('pic_name') or '').strip()
            client_pic_no = (request.POST.get('pic_no') or '').strip()
            upfile = request.FILES.get('pic_file')
            if not upfile:
                return JsonResponse({'status': 'error', 'message': 'ไม่พบไฟล์ (pic_file)'}, status=400)

            user_specific_path = f'img/user_{request.user.username}/{upfile.name}'
            saved_relative_path = default_storage.save(user_specific_path, upfile)
            saved_url = default_storage.url(saved_relative_path)

            picture_block = {
                "pic_no": client_pic_no,
                "pic_name": pic_name,
                "pic_path": saved_relative_path,
                "pic_url": saved_url
            }
            return JsonResponse({"status": "ok", "message": "อัปโหลดรูปสำเร็จ", "picture": picture_block})
        except Exception:
            return JsonResponse(
                {'status': 'error', 'message': 'Upload failed', 'trace': traceback.format_exc()},
                status=500
            )

    if action == 'save':
        secs_in   = safe_parse_list(raw_secs, db_secs)
        tables_in = safe_parse_list(raw_tables, db_tables)
        try:
            DocChapter3.objects.update_or_create(
                user=user,
                defaults={
                    'chap_id': 3,
                    'intro_body': intro_body,
                    'sections_json': secs_in,
                    'tb_sections_json': tables_in,
                    'updated_at': timezone.now(),
                }
            )
            # ใช้ extra_tags เพื่อกันปนกับหน้าบทอื่น
            messages.success(request, '💾 บันทึกข้อมูลบทที่ 3 เรียบร้อยแล้ว', extra_tags='chapter3')
        except IntegrityError as e:
            messages.error(request, f'IntegrityError: {e}', extra_tags='chapter3')
        except Exception as e:
            messages.error(request, f'Error: {e}', extra_tags='chapter3')
        return redirect(request.path)

    if action == 'get_data':
        # แค่รีเฟรชหน้าให้ดึงค่า db ล่าสุด
        messages.info(request, '🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว', extra_tags='chapter3')
        return redirect(request.path)

    if action == 'generate_doc':
        try:
            sections_in = safe_parse_list(raw_secs, db_secs)
            tables_in   = safe_parse_list(raw_tables, db_tables)

            def extractAllPictures(sections_list):
                pics = []
                def walkNode(node):
                    if not isinstance(node, dict): return
                    if isinstance(node.get("pictures"), list):
                        pics.extend([p for p in node["pictures"] if p])
                    if isinstance(node.get("children"), list):
                        for ch in node["children"]:
                            walkNode(ch)
                if isinstance(sections_list, list):
                    for sec in sections_list:
                        if not isinstance(sec, dict): continue
                        if isinstance(sec.get("pictures"), list):
                            pics.extend([p for p in sec["pictures"] if p])
                        if isinstance(sec.get("items"), list):
                            for node in sec["items"]:
                                walkNode(node)
                def seq(p):
                    try:
                        return int(str(p.get("pic_no","0-0")).split("-")[-1])
                    except Exception:
                        return 0
                pics.sort(key=seq)
                return pics

            all_pics = extractAllPictures(sections_in)

            if generate_doc_ch3 is None:
                messages.error(request, "ยังไม่ได้ติดตั้งตัวสร้างเอกสารของบทที่ 3 (man_doc/doc_chapter3.py)", extra_tags='chapter3')
                return redirect(request.path)

            doc = generate_doc_ch3(
                intro_body=intro_body or db_intro,
                sections_json=sections_in,
                tables_json=tables_in,
                pictures=all_pics,
                media_root=settings.MEDIA_ROOT
            )
            bio = BytesIO()
            doc.save(bio)
            bio.seek(0)
            resp = FileResponse(
                bio,
                as_attachment=True,
                filename="chapter3.docx",
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            resp["Cache-Control"] = "no-store"
            return resp

        except Exception:
            messages.error(request, f'Generate failed: {traceback.format_exc()}', extra_tags='chapter3')
            return redirect(request.path)

    messages.error(request, f'unknown action "{action}"', extra_tags='chapter3')
    return redirect(request.path)
# ========= จบส่วนบทที่ 3 =========


def chapter_4_view(request):
    return render(request, 'chapter_4.html')

def chapter_5_view(request):
    return chapter_5_view_logic(request)

def home_view(request):
    return render(request, 'home.html')

def terms_view(request):
    return render(request, "legal/terms_of_use.html")

def privacy_view(request):
    return render(request, "legal/privacy_policy.html")





# ---------------- บทคัดย่อ + กิตติกรรมประกาศ ----------------
@login_required
def abstract_ack_view(request):
    user = request.user
    initial = {}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'get_data_intro':
            messages.success(request, 'ดึงข้อมูลล่าสุดสำเร็จแล้ว')
            return redirect('abstract_ack_view')

        elif action == 'save_intro':
            form_data = {
                'total_pages': request.POST.get('total_pages') or None,
                'keyword_th': request.POST.get('keyword_th', ''),
                'keyword_en': request.POST.get('keyword_en', ''),
                'abstract_th_json': json.loads(request.POST.get('abstract_th_json', '[]')),
                'abstract_en_json': json.loads(request.POST.get('abstract_en_json', '[]')),
                'acknow_json': json.loads(request.POST.get('acknowledgement_json', '[]')),
            }
            DocAbstract.objects.update_or_create(user=user, defaults=form_data)
            messages.success(request, 'บันทึกข้อมูลเรียบร้อยแล้ว')
            return redirect('abstract_ack_view')

        elif action == 'generate_intro':
            try:
                intro_data = DocIntroduction.objects.get(user=user)
                abstract_data = DocAbstract.objects.get(user=user)

                full_data_for_docx = {
                    'project_name_th': intro_data.name_pro_th,
                    'project_name_en': intro_data.name_pro_en,
                    'major_th': intro_data.dep_th,
                    'major_en': intro_data.dep_en,
                    'advisor_th': intro_data.advisor_th,
                    'advisor_en': intro_data.advisor_en,
                    'coadvisor_th': intro_data.coadvisor_th,
                    'coadvisor_en': intro_data.coadvisor_en,
                    'academic_year_th': intro_data.school_y_BE,
                    'academic_year_en': intro_data.school_y_AD,
                    'student_names': intro_data.student_name or [],

                    'total_pages': abstract_data.total_pages,
                    'keyword_th': abstract_data.keyword_th,
                    'keyword_en': abstract_data.keyword_en,
                    'abstract_th_paragraphs': abstract_data.abstract_th_json,
                    'abstract_en_paragraphs': abstract_data.abstract_en_json,
                    'acknowledgement_paragraphs': abstract_data.acknow_json,
                }
                doc = doc_abstract_ack(full_data_for_docx)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename=abstract_and_acknow.docx'
                doc.save(response)
                return response
            except (DocIntroduction.DoesNotExist, DocAbstract.DoesNotExist):
                messages.error(request, 'ไม่สามารถสร้างไฟล์ได้ เนื่องจากข้อมูลโครงงานหรือบทคัดย่อไม่ครบถ้วน')
                return redirect('abstract_ack_view')

    # GET
    try:
        data_from_introduction = DocIntroduction.objects.get(user=user)
        initial = {
            'project_name_th': data_from_introduction.name_pro_th,
            'project_name_en': data_from_introduction.name_pro_en,
            'major_th': data_from_introduction.dep_th,
            'major_en': data_from_introduction.dep_en,
            'advisor_th': data_from_introduction.advisor_th,
            'advisor_en': data_from_introduction.advisor_en,
            'coadvisor_th': data_from_introduction.coadvisor_th,
            'coadvisor_en': data_from_introduction.coadvisor_en,
            'academic_year_th': data_from_introduction.school_y_BE,
            'academic_year_en': data_from_introduction.school_y_AD,
        }
        initial['student_names'] = data_from_introduction.student_name or []
    except DocIntroduction.DoesNotExist:
        messages.warning(request, 'กรุณากรอกข้อมูลโครงงานในหน้าแรกก่อน')

    try:
        abstract_data = DocAbstract.objects.get(user=user)
        initial.update({
            'total_pages': abstract_data.total_pages,
            'keyword_th': abstract_data.keyword_th,
            'keyword_en': abstract_data.keyword_en,
            'abstract_th_json': json.dumps(abstract_data.abstract_th_json, ensure_ascii=False),
            'abstract_en_json': json.dumps(abstract_data.abstract_en_json, ensure_ascii=False),
            'acknowledgement_json': json.dumps(abstract_data.acknow_json, ensure_ascii=False),
        })
    except DocAbstract.DoesNotExist:
        pass

    return render(request, 'abstract_ack.html', {'initial': initial})


# ---------------- ใบรับรอง ----------------
@login_required
def certificate_view(request):
    user = request.user
    uid = current_user_id(request)
    intro = DocIntroduction.objects.filter(user_id=uid).first()
    if not intro:
        messages.error(request, "ยังไม่มีข้อมูล Project Setup กรุณากรอกก่อน")
        return redirect('project_setup')

    action = request.POST.get('action', '')
    initial = {}

    if request.method == 'POST':
        if action == 'get_certificate':
            try:
                cert = DocIntroduction.objects.get(user=user)
                initial = {
                    'comm_dean': cert.comm_dean,
                    'comm_prathan': cert.comm_prathan,
                    'comm_first': cert.comm_first,
                    'comm_sec': cert.comm_sec,
                }
                messages.success(request, 'ดึงข้อมูลสำเร็จ')
            except DocIntroduction.DoesNotExist:
                messages.info(request, 'ยังไม่มีข้อมูล')
            return render(request, 'certificate.html', {'initial': initial})

        elif action == 'save_certificate':
            form_data = {
                'comm_dean': request.POST.get('comm_dean', '').strip(),
                'comm_prathan': request.POST.get('comm_prathan', '').strip(),
                'comm_first': request.POST.get('comm_first', '').strip(),
                'comm_sec': request.POST.get('comm_sec', '').strip(),
            }
            DocIntroduction.objects.update_or_create(user=user, defaults=form_data)
            messages.success(request, 'บันทึกข้อมูลกรรมการเรียบร้อยแล้ว')
            return redirect('certificate')

        elif action == 'generate_certificate':
            project_name_th = intro.name_pro_th or ""
            author1_th, author2_th, author1_en, author2_en = _authors_from_intro(intro)

            cert = DocIntroduction.objects.filter(user=user).first()
            comm_dean = cert.comm_dean if cert else ''
            prathan = cert.comm_prathan if cert else ''
            comm_first = cert.comm_first if cert else ''
            comm_sec = cert.comm_sec if cert else ''

            doc = doc_certificate(project_name_th, author1_th, author2_th, comm_dean, prathan, comm_first, comm_sec)
            buf = BytesIO()
            doc.save(buf)
            buf.seek(0)
            return FileResponse(buf, as_attachment=True, filename='Certificate.docx')

    return render(request, 'certificate.html', {'initial': initial})


# ---------------- บรรณานุกรม ----------------
@login_required
def refer_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        references = collect_references_from_post(request)

        if action == 'save_refer':
            save_websites_from_refs(request.user, references)
            save_books_from_refs(request.user, references)

            initial_refs = initial_refs_web_from_db(request.user) + initial_books_from_db(request.user)
            ctx = {'initial_refs_json': json.dumps(initial_refs, ensure_ascii=False)}
            messages.success(request, f'บันทึกข้อมูลสำเร็จ {len(initial_refs)} รายการ')
            return render(request, 'refer.html', ctx)

        if action == 'generate_refer':
            save_websites_from_refs(request.user, references)
            save_books_from_refs(request.user, references)
            refs_for_doc = format_dates_for_doc(references)
            doc = doc_refer(refs_for_doc)
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = 'attachment; filename=references.docx'
            doc.save(response)
            return response

        if action == 'get_data':
            initial_refs = initial_refs_web_from_db(request.user) + initial_books_from_db(request.user)
            ctx = {'initial_refs_json': json.dumps(initial_refs, ensure_ascii=False)}
            return render(request, 'refer.html', ctx)

    return render(request, 'refer.html')


# ---------------- บทที่ 5 ----------------

# ---------------- Project Setup ----------------
def _parse_lines_to_list(text):
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]

@transaction.atomic
def project_setup_view(request):
    uid = current_user_id(request)
    if not uid:
        return render(request, 'project_setup.html', {
            'initial': {'error': 'ไม่พบ user_id กรุณาเข้าสู่ระบบหรือลองใหม่'}
        })

    intro = DocIntroduction.objects.filter(user_id=uid).first()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'get_data':
            initial = {}
            if intro:
                student_name = intro.student_name or {}
                authors_th = student_name.get('th', []) if isinstance(student_name, dict) else []
                authors_en = student_name.get('en', []) if isinstance(student_name, dict) else []

                def to_str(v):
                    if v is None:
                        return ''
                    if isinstance(v, (list, dict)):
                        try:
                            return ', '.join(v) if isinstance(v, list) else json.dumps(v, ensure_ascii=False)
                        except Exception:
                            return json.dumps(v, ensure_ascii=False)
                    return str(v)

                initial.update({
                    'name_pro_th': intro.name_pro_th or '',
                    'name_pro_en': intro.name_pro_en or '',
                    'dep_th': intro.dep_th or '',
                    'dep_en': intro.dep_en or '',
                    'school_y_BE': intro.school_y_BE or '',
                    'school_y_AD': intro.school_y_AD or '',
                    'advisor_th': intro.advisor_th or '',
                    'advisor_en': intro.advisor_en or '',
                    'coadvisor_th': to_str(intro.coadvisor_th),
                    'coadvisor_en': to_str(intro.coadvisor_en),
                    'authors_th_json': json.dumps(authors_th, ensure_ascii=False),
                    'authors_en_json': json.dumps(authors_en, ensure_ascii=False),
                    'authors_th': authors_th,
                    'authors_en': authors_en,
                })
            else:
                initial.update({
                    'authors_th_json': '[]',
                    'authors_en_json': '[]',
                    'authors_th': [],
                    'authors_en': [],
                })
            return render(request, 'project_setup.html', {'initial': initial})

        elif action == 'save_setup':
            authors_th, authors_en = [], []
            for i in range(1, 4):
                th = (request.POST.get(f'name_author_th_{i}', '') or '').strip()
                en = (request.POST.get(f'name_author_en_{i}', '') or '').strip()
                if th or en:
                    authors_th.append(th)
                    authors_en.append(en)

            student_name = {'th': authors_th, 'en': authors_en}

            def to_int(v):
                v = (v or '').strip()
                return int(v) if v.isdigit() else None

            def to_json_primitive_str(v):
                v = (v or '').strip()
                if not v:
                    return None
                return v

            defaults = {
                'name_pro_th': (request.POST.get('name_pro_th') or '').strip(),
                'name_pro_en': (request.POST.get('name_pro_en') or '').strip(),
                'dep_th': (request.POST.get('dep_th') or '').strip(),
                'dep_en': (request.POST.get('dep_en') or '').strip(),
                'school_y_BE': to_int(request.POST.get('school_y_BE')),
                'school_y_AD': to_int(request.POST.get('school_y_AD')),
                'advisor_th': (request.POST.get('advisor_th') or '').strip(),
                'advisor_en': (request.POST.get('advisor_en') or '').strip(),
                'coadvisor_th': to_json_primitive_str(request.POST.get('coadvisor_th')),
                'coadvisor_en': to_json_primitive_str(request.POST.get('coadvisor_en')),
                'student_name': student_name,
            }

            obj, created = DocIntroduction.objects.update_or_create(
                user_id=uid,
                defaults=defaults
            )

            if not is_intro_ok_check(obj):
                messages.warning(request, 'กรุณากรอกอย่างน้อย: ชื่อโครงงาน (TH/EN) และชื่อผู้จัดทำอย่างน้อย 1 คน')
                return redirect(reverse('project_setup'))

            messages.success(request, 'บันทึกข้อมูล Project Setup สำเร็จ')
            return redirect(reverse('project_setup'))

        elif action == 'go_index':
            return render(request, 'index.html')

    # GET
    initial = {}
    if intro:
        st = intro.student_name or {}
        authors_th = st.get('th', []) if isinstance(st, dict) else []
        authors_en = st.get('en', []) if isinstance(st, dict) else []

        def to_str(v):
            if v is None:
                return ''
            if isinstance(v, (list, dict)):
                try:
                    return ', '.join(v) if isinstance(v, list) else json.dumps(v, ensure_ascii=False)
                except Exception:
                    return json.dumps(v, ensure_ascii=False)
            return str(v)

        initial.update({
            'name_pro_th': intro.name_pro_th or '',
            'name_pro_en': intro.name_pro_en or '',
            'dep_th': intro.dep_th or '',
            'dep_en': intro.dep_en or '',
            'school_y_BE': intro.school_y_BE or '',
            'school_y_AD': intro.school_y_AD or '',
            'advisor_th': intro.advisor_th or '',
            'advisor_en': intro.advisor_en or '',
            'coadvisor_th': to_str(intro.coadvisor_th),
            'coadvisor_en': to_str(intro.coadvisor_en),
            'authors_th_json': json.dumps(authors_th, ensure_ascii=False),
            'authors_en_json': json.dumps(authors_en, ensure_ascii=False),
            'authors_th': authors_th,
            'authors_en': authors_en,
        })
    else:
        initial.update({
            'authors_th_json': '[]',
            'authors_en_json': '[]',
            'authors_th': [],
            'authors_en': [],
        })

    return render(request, 'project_setup.html', {'initial': initial})


# ---------------- Manage DOC (ปุ่มดาวน์โหลดหน้าปก) ----------------
@login_required
def manage_doc_view(request):
    uid = getattr(request.user, 'pk', None)
    if not uid:
        messages.error(request, "กรุณาเข้าสู่ระบบก่อน")
        return redirect('login')

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()

        intro = DocIntroduction.objects.filter(user_id=uid).first()
        if not intro:
            messages.error(request, "ยังไม่มีข้อมูลโครงงาน กรุณากรอกที่หน้า Project Setup ก่อน")
            return render(request, 'manage_doc.html', {})

        project_name_th = intro.name_pro_th or ""
        project_name_en = intro.name_pro_en or ""
        dep_th = intro.dep_th or ""
        dep_en = intro.dep_en or ""
        author1_th, author2_th, author1_en, author2_en = _authors_from_intro(intro)

        academic_year_be = intro.school_y_BE or 0
        academic_year_for_en = academic_year_be  # doc_cover_en แปลง ค.ศ. ภายในแล้ว

        if action == 'generate_cover_th':
            doc = doc_cover_th(project_name_th, project_name_en,
                               author1_th, author2_th,
                               author1_en, author2_en,
                               academic_year_be, dep_th)
            resp = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            resp['Content-Disposition'] = 'attachment; filename=cover_th.docx'
            doc.save(resp)
            return resp

        elif action == 'generate_cover_en':
            doc = doc_cover_en(project_name_th, project_name_en,
                               author1_th, author2_th,
                               author1_en, author2_en,
                               academic_year_for_en, dep_en)
            resp = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            resp['Content-Disposition'] = 'attachment; filename=cover_en.docx'
            doc.save(resp)
            return resp

        elif action == 'generate_cover_sec':
            doc = doc_cover_sec(project_name_th, project_name_en,
                                author1_th, author2_th,
                                author1_en, author2_en,
                                academic_year_be, dep_th)
            resp = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            resp['Content-Disposition'] = 'attachment; filename=cover_sec.docx'
            doc.save(resp)
            return resp

        else:
            messages.error(request, "ไม่พบ action ที่รองรับ")

    return render(request, 'manage_doc.html', {})
