# backend/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db import transaction
from django.urls import reverse

import json
import re
import copy
from io import BytesIO

# Forms / Models
from .forms import RegisterForm, LoginForm
from .models import (
    SpProject, SpProjectAuthor, DocCover, Certificate, Chapter1, RefWebsite, RefBook,
    Chapter5, DocIntroduction, DocAbstract
)

# DOCX builders
from man_doc.doc_sp_01 import doc_sp_01
from man_doc.doc_cover import doc_cover_th, doc_cover_en, doc_cover_sec
from man_doc.doc_abstract_ack import doc_abstract_ack
from man_doc.doc_refer import doc_refer
from man_doc.doc_chapter5 import doc_chapter5
from man_doc.doc_chapter1 import doc_chapter1
from man_doc.doc_certificate import doc_certificate

# ====== imports from man_views (helpers ที่แยกออก) ======
from man_views.views_current_user_id import current_user_id as _current_user_id
from man_views.views_is_intro_ok_check import is_intro_ok_check
from man_views.views_authors_from_intro import authors_from_intro as _authors_from_intro

# รวม helper อ้างอิง (ตามไฟล์ที่คุณรวม)
from webdoc.webdoc.man_views.views_save_refs import save_websites_from_refs, save_books_from_refs
from man_views.views_initial_refs import initial_refs_web_from_db, initial_books_from_db

from man_views.views_format_dates_for_doc import format_dates_for_doc
from man_views.views_collect_references import collect_references_from_post
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
            return redirect('webdoc:index')
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

def cover(request):
    return render(request, 'cover.html')

def sp_project_form_view(request):
    return render(request, 'sp_project_form.html')

def intro_view(request):
    return render(request, 'intro.html')

def chapter_1_view(request):
    return render(request, 'chapter_1.html')

def chapter_2_view(request):
    return render(request, 'chapter_2.html')

def chapter_3_view(request):
    return render(request, 'chapter_3.html')

def chapter_4_view(request):
    return render(request, 'chapter_4.html')

def refer_view(request):
    return render(request, 'refer.html')

def home_view(request):
    return render(request, 'home.html')

def terms_view(request):
    return render(request, "legal/terms_of_use.html")

def privacy_view(request):
    return render(request, "legal/privacy_policy.html")


# ---------------- แบบฟอร์ม ทก.01 ----------------
@login_required
def sp_project_form_view(request):
    user = request.user
    initial = {}
    status_message = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'get_data':
            try:
                project = SpProject.objects.get(user=user)
                initial = {
                    'name_pro_th': project.name_pro_th,
                    'name_pro_en': project.name_pro_en,
                    'case_stu': project.case_stu,
                    'term': project.term,
                    'school_y': project.school_y,
                    'adviser': project.adviser,
                    'co_advisor': project.co_advisor,
                    'strategic': project.strategic,
                    'plan': project.plan,
                    'key_result': project.key_result,
                    'bg_and_sig_para1': project.bg_and_sig_para1,
                    'bg_and_sig_para2': project.bg_and_sig_para2,
                    'bg_and_sig_para3': project.bg_and_sig_para3,
                    'purpose_1': project.purpose_1,
                    'purpose_2': project.purpose_2,
                    'purpose_3': project.purpose_3,
                    'authors': list(
                        SpProjectAuthor.objects.filter(user=user, project=project)
                        .values_list('name', flat=True)
                    ),
                }
                authors = list(
                    SpProjectAuthor.objects.filter(userid=user.user_id, project=project)
                    .values_list('name', flat=True)
                )
                initial['authors'] = authors
                status_message = {'message': '✅ ดึงข้อมูลสำเร็จแล้ว!', 'type': 'success'}
            except SpProject.DoesNotExist:
                initial = {}
                status_message = {'message': 'ยังไม่มีข้อมูล', 'type': 'info'}

        elif action in ('save', 'generate'):
            # อ่านค่าจากฟอร์ม
            name_pro_th   = request.POST.get('name_pro_th', '')
            name_pro_en   = request.POST.get('name_pro_en', '')
            case_stu      = request.POST.get('case_stu', '')
            term          = request.POST.get('term', '')
            school_y      = request.POST.get('school_y', '')
            adviser       = request.POST.get('adviser', '')
            co_advisor    = request.POST.get('co_advisor', '')
            strategic     = request.POST.get('strategic', '')
            plan          = request.POST.get('plan', '')
            key_result    = request.POST.get('key_result', '')
            bg_and_sig_para1 = request.POST.get('bg_and_sig_para1', '')
            bg_and_sig_para2 = request.POST.get('bg_and_sig_para2', '')
            bg_and_sig_para3 = request.POST.get('bg_and_sig_para3', '')
            purpose_1 = request.POST.get('purpose_1', '')
            purpose_2 = request.POST.get('purpose_2', '')
            purpose_3 = request.POST.get('purpose_3', '')
            # authors list
            authors = []
            try:
                authors = json.loads(request.POST.get('authors_json', '[]'))
            except Exception:
                pass

            if action == 'save':
                project, created = SpProject.objects.update_or_create(
                    user=user,
                    defaults={
                        'name_pro_th': name_pro_th,
                        'name_pro_en': name_pro_en,
                        'case_stu': case_stu,
                        'term': term,
                        'school_y': school_y,
                        'adviser': adviser,
                        'co_advisor': co_advisor,
                        'strategic': strategic,
                        'plan': plan,
                        'key_result': key_result,
                        'bg_and_sig_para1': bg_and_sig_para1,
                        'bg_and_sig_para2': bg_and_sig_para2,
                        'bg_and_sig_para3': bg_and_sig_para3,
                        'purpose_1': purpose_1,
                        'purpose_2': purpose_2,
                        'purpose_3': purpose_3,
                    }
                )
                SpProjectAuthor.objects.filter(user=user, project=project).delete()
                for name in authors:
                    SpProjectAuthor.objects.create(user=user, name=name, project=project)

                initial = {
                    'name_pro_th': name_pro_th,
                    'name_pro_en': name_pro_en,
                    'case_stu': case_stu,
                    'term': term,
                    'school_y': school_y,
                    'adviser': adviser,
                    'co_advisor': co_advisor,
                    'strategic': strategic,
                    'plan': plan,
                    'key_result': key_result,
                    'bg_and_sig_para1': bg_and_sig_para1,
                    'bg_and_sig_para2': bg_and_sig_para2,
                    'bg_and_sig_para3': bg_and_sig_para3,
                    'purpose_1': purpose_1,
                    'purpose_2': purpose_2,
                    'purpose_3': purpose_3,
                    'authors': authors,
                }
                status_message = {'message': '✅ บันทึกข้อมูลสำเร็จแล้ว!', 'type': 'success'}

            elif action == 'generate':
                doc = doc_sp_01(
                    name_pro_th, name_pro_en, authors,
                    case_stu, term, school_y,
                    adviser, co_advisor,
                    strategic, plan, key_result,
                    bg_and_sig_para1, bg_and_sig_para2, bg_and_sig_para3,
                    purpose_1, purpose_2, purpose_3,
                )
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename=sp_project_form.docx'
                doc.save(response)
                return response

    if request.path.endswith('/sp_project_form_2/'):
        return render(request, 'sp_project_form_2.html', {'initial': initial, 'status_message': status_message})
    else:
        return render(request, 'sp_project_form.html', {'initial': initial, 'status_message': status_message})


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
    uid = _current_user_id(request)
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


# ---------------- บทที่ 1 ----------------
@login_required
def chapter_1_view(request):
    user = request.user
    initial = {}
    status_message = None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'get_data':
            try:
                chapter1_data = Chapter1.objects.get(user=user)
                initial = {
                    'sec11_p1': chapter1_data.sec11_p1,
                    'sec11_p2': chapter1_data.sec11_p2,
                    'sec11_p3': chapter1_data.sec11_p3,
                    'purpose_count': chapter1_data.purpose_count,
                    'purpose_1': chapter1_data.purpose_1,
                    'purpose_2': chapter1_data.purpose_2,
                    'purpose_3': chapter1_data.purpose_3,
                    'hypo_paragraph': chapter1_data.hypo_paragraph,
                    'hypo_items_json': chapter1_data.hypo_items_json,
                    'scope_json': chapter1_data.scope_json,
                    'para_premise': chapter1_data.para_premise,
                    'premise_json': chapter1_data.premise_json,
                    'def_items_json': chapter1_data.def_items_json,
                    'benefit_items_json': chapter1_data.benefit_items_json,
                }
                status_message = {'message': '✅ ดึงข้อมูลสำเร็จแล้ว!', 'type': 'success'}
            except Chapter1.DoesNotExist:
                initial = {}
                status_message = {'message': 'ไม่มีข้อมูลอยู่ กรุณากรอกข้อมูลแล้วบันทึก!', 'type': 'warning'}

        elif action in ('save', 'generate'):
            sec11_p1 = request.POST.get('sec11_p1', '')
            sec11_p2 = request.POST.get('sec11_p2', '')
            sec11_p3 = request.POST.get('sec11_p3', '')

            try:
                purpose_count = int(request.POST.get('purpose_count', 0))
            except Exception:
                purpose_count = 0

            purpose_1 = request.POST.get('purpose_1', '')
            purpose_2 = request.POST.get('purpose_2', '')
            purpose_3 = request.POST.get('purpose_3', '')

            hypo_paragraph = request.POST.get('hypo_paragraph', '')
            hypo_items     = json.loads(request.POST.get('hypo_items_json', '[]'))
            scope_data     = json.loads(request.POST.get('scope_json', '[]'))
            para_premise_str = request.POST.get('para_premise', '')
            premise_data   = json.loads(request.POST.get('premise_json', '[]'))
            def_items      = json.loads(request.POST.get('def_items_json', '[]'))
            benefit_items  = json.loads(request.POST.get('benefit_items_json', '[]'))

            if action == 'save':
                Chapter1.objects.update_or_create(
                    user=user,
                    defaults={
                        'sec11_p1': sec11_p1,
                        'sec11_p2': sec11_p2,
                        'sec11_p3': sec11_p3,
                        'purpose_count': purpose_count,
                        'purpose_1': purpose_1,
                        'purpose_2': purpose_2,
                        'purpose_3': purpose_3,
                        'hypo_paragraph': hypo_paragraph,
                        'hypo_items_json': hypo_items,
                        'scope_json': scope_data,
                        'para_premise': para_premise_str,
                        'premise_json': premise_data,
                        'def_items_json': def_items,
                        'benefit_items_json': benefit_items,
                    }
                )
                status_message = {'message': '✅ บันทึกข้อมูลสำเร็จแล้ว!', 'type': 'success'}

            elif action == 'generate':
                doc = doc_chapter1(
                    sec11_p1, sec11_p2, sec11_p3, purpose_count, purpose_1, purpose_2, purpose_3,
                    hypo_paragraph, hypo_items, scope_data, para_premise_str, premise_data, def_items, benefit_items
                )
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename=chapter1.docx'
                doc.save(response)
                return response

            initial = {
                'sec11_p1': sec11_p1,
                'sec11_p2': sec11_p2,
                'sec11_p3': sec11_p3,
                'purpose_count': purpose_count,
                'purpose_1': purpose_1,
                'purpose_2': purpose_2,
                'purpose_3': purpose_3,
                'hypo_paragraph': hypo_paragraph,
                'hypo_items_json': hypo_items,
                'scope_json': scope_data,
                'para_premise': para_premise_str,
                'premise_json': premise_data,
                'def_items_json': def_items,
                'benefit_items_json': benefit_items,
            }

    context = {'initial': initial, 'status_message': status_message}
    return render(request, 'chapter_1.html', context)


# ---------------- บทที่ 5 ----------------
DEFAULT_TITLES = ['สรุปผลการดำเนินงาน', 'อภิปรายผล', 'ข้อเสนอแนะ']
DEFAULT_SECTIONS = [
    {"title": DEFAULT_TITLES[0], "body": "", "mains": []},
    {"title": DEFAULT_TITLES[1], "body": "", "mains": []},
    {"title": DEFAULT_TITLES[2], "body": "", "mains": []},
]

def _norm(s: str) -> str:
    return re.sub(r'\s+', ' ', (s or '')).strip()

def _get_title(d: dict) -> str:
    if not isinstance(d, dict): return ''
    for k in ('title', 'name', 'header'):
        v = (d.get(k) or '').strip()
        if v: return v
    return ''

def _get_body(d: dict) -> str:
    if not isinstance(d, dict): return ''
    for k in ('body', 'intro', 'content', 'paragraph', 'desc', 'text'):
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return ''

def _to_mains_list(d: dict):
    if not isinstance(d, dict): return []
    candidates = d.get('mains')
    if candidates is None: candidates = d.get('items')
    if candidates is None: candidates = d.get('children')
    if not isinstance(candidates, list): return []
    out = []
    for m in candidates:
        if isinstance(m, dict):
            text = _get_title(m) or (m.get('text') or '').strip()
            subs = m.get('subs')
            if subs is None: subs = m.get('children')
            if subs is None: subs = m.get('items')
            if not isinstance(subs, list): subs = []
            norm_subs = []
            for s in subs:
                if isinstance(s, dict):
                    sv = (s.get('text') or s.get('title') or s.get('name') or '').strip()
                    if sv: norm_subs.append(sv)
                elif isinstance(s, str):
                    sv = s.strip()
                    if sv: norm_subs.append(sv)
            out.append({"text": text, "subs": norm_subs})
        elif isinstance(m, str):
            out.append({"text": m.strip(), "subs": []})
    return out

def _normalize_and_order(sections, intro_body, prev=None):
    prev = prev or []
    norm_list = []

    if not isinstance(sections, list) or not sections:
        sections = copy.deepcopy(DEFAULT_SECTIONS)

    for i, raw in enumerate(sections):
        sec = raw if isinstance(raw, dict) else {}
        title = _get_title(sec) or ''
        if not title and i < len(prev) and isinstance(prev[i], dict):
            title = _get_title(prev[i]) or ''
        if not title and i < len(DEFAULT_TITLES):
            title = DEFAULT_TITLES[i]

        body = _get_body(sec)
        mains = _to_mains_list(sec)

        for j, m in enumerate(mains):
            m['main_order'] = j + 1

        norm_list.append({
            "title": title or "",
            "body": body or "",
            "mains": mains,
            "section_order": i + 1,
        })
    return norm_list

def _sorted_with_numbers(sections):
    if not isinstance(sections, list): return []
    sections = sorted(sections, key=lambda s: int(s.get('section_order') or 0))

    for i, sec in enumerate(sections, start=1):
        sec['no'] = f'5.{i}'
        title = _get_title(sec)
        sec.setdefault('title', title or '')
        sec.setdefault('name',  title or sec['title'])
        sec.setdefault('header',title or sec['title'])

        mains = sec.get('mains') if isinstance(sec.get('mains'), list) else []
        mains = sorted(mains, key=lambda m: int(m.get('main_order') or 0))
        for j, m in enumerate(mains, start=1):
            m['no'] = f'5.{i}.{j}'
            new_subs = []
            subs = m.get('subs') if isinstance(m.get('subs'), list) else []
            for k, s in enumerate(subs, start=1):
                text = (s or '').strip() if isinstance(s, str) else ''
                if text:
                    new_subs.append({"text": text, "no": f'5.{i}.{j}.{k}'})
            m['subs'] = new_subs
        sec['mains'] = mains
    return sections

def _sections_from_ui_json(raw_json: str, fallback_list):
    try:
        data = json.loads(raw_json) if raw_json else []
    except json.JSONDecodeError:
        data = []
    if not isinstance(data, list) or not data:
        data = fallback_list or []

    out = []
    for s in data:
        if not isinstance(s, dict):
            continue
        title = (s.get('title') or s.get('header') or s.get('name') or '').strip()
        body  = (s.get('body')  or s.get('content') or s.get('desc')  or '').strip()

        points = s.get('points') or s.get('mains') or s.get('items') or []
        mains = []
        if isinstance(points, list):
            for p in points:
                if isinstance(p, dict):
                    text = (p.get('main') or p.get('text') or p.get('title') or '').strip()
                    subs_src = p.get('subs') or p.get('children') or p.get('items') or []
                    subs = []
                    if isinstance(subs_src, list):
                        for sub in subs_src:
                            if isinstance(sub, str):
                                st = sub.strip()
                                if st: subs.append(st)
                            elif isinstance(sub, dict):
                                st = (sub.get('text') or sub.get('title') or sub.get('name') or '').strip()
                                if st: subs.append(st)
                    mains.append({'text': text, 'subs': subs})
                elif isinstance(p, str):
                    t = p.strip()
                    if t: mains.append({'text': t, 'subs': []})

        out.append({'title': title, 'body': body, 'mains': mains})
    return out

@login_required
def chapter_5_view(request):
    user = request.user

    row = Chapter5.objects.filter(user=user).order_by('-updated_at').first()
    db_intro = (row.intro_th if row else '') or ''
    db_sections = row.sections_json if (row and isinstance(row.sections_json, list)) else []

    def safe_parse_list(raw: str, default: list):
        try:
            data = json.loads(raw or '[]')
            return data if isinstance(data, list) else (default or [])
        except json.JSONDecodeError:
            return default or []

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()
        intro_body = (request.POST.get('intro_body') or '').strip()
        raw_json = request.POST.get('chapter5_json', '')

        if action == 'save':
            sections_in = safe_parse_list(raw_json, [])
            Chapter5.objects.update_or_create(
                user=user,
                defaults={
                    'intro_th': intro_body,
                    'sections_json': sections_in,
                    'updated_at': timezone.now(),
                }
            )
            messages.success(request, '💾 บันทึกข้อมูลบทที่ 5 เรียบร้อยแล้ว')
            return render(request, 'chapter_5.html', {
                'initial': {'intro_body': '', 'chapter5_json': []}
            })

        elif action == 'get_data':
            messages.info(request, '🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว')
            return render(request, 'chapter_5.html', {
                'initial': {'intro_body': db_intro, 'chapter5_json': db_sections}
            })

        elif action == 'generate_docx':
            sections_for_doc = safe_parse_list(raw_json, db_sections)
            if not intro_body:
                intro_body = db_intro

            doc = doc_chapter5(intro_body, sections_for_doc)
            buf = BytesIO()
            doc.save(buf)
            buf.seek(0)
            return FileResponse(
                buf,
                as_attachment=True,
                filename='chapter5.docx',
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

        messages.info(request, 'ยังไม่รองรับการทำงานนี้')
        return render(request, 'chapter_5.html', {
            'initial': {'intro_body': '', 'chapter5_json': []}
        })

    return render(request, 'chapter_5.html', {
        'initial': {
            'intro_body': (db_intro if (db_intro or db_sections) else ''),
            'chapter5_json': (db_sections if isinstance(db_sections, list) else []),
        }
    })


# ---------------- Project Setup ----------------
def _parse_lines_to_list(text):
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]

@transaction.atomic
def project_setup_view(request):
    uid = _current_user_id(request)
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
