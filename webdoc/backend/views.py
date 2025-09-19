from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .forms import RegisterForm, LoginForm
from .models import SpProject, SpProjectAuthor, DocCover, Abstract , Certificate ,Chapter1,RefWebsite ,RefBook
from man_doc.doc_sp_01 import doc_sp_01
from man_doc.doc_cover import doc_cover_th, doc_cover_en, doc_cover_sec  
from man_doc.doc_intro import doc_intro  
from man_doc.doc_refer import doc_refer  
from django.template.loader import render_to_string
from man_doc.doc_chapter1 import doc_chapter1
from django.utils.dateparse import parse_date
import io
from django.http import FileResponse
from man_doc.doc_certificate import doc_certificate
from django.utils.dateparse import parse_date

# Register / Login / Logout
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(request, email=email, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()  # จากฟอร์ม login
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

# Static Pages
@login_required
def index(request):
    return render(request, 'index.html')

def manage_doc(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'index.html')

def cover(request):
    return render(request, 'cover.html')

def sp_project_form_view(request):
    return render(request, 'sp_project_form.html')

def sp_project_form_2_view(request):
    return render(request, 'sp_project_form_2.html')

def intro_view(request):
    return render(request, 'intro.html')

def certificate_view(request):
    initial = {}
    return render(request, 'certificate.html', {'initial': initial})

def chapter_1_view(request):
    return render(request, 'chapter_1.html')

def chapter_2_view(request):
    return render(request, 'chapter_2.html')

def chapter_3_view(request):
    return render(request, 'chapter_3.html')

def chapter_4_view(request):
    return render(request, 'chapter_4.html')

def chapter_5_view(request):
    return render(request, 'chapter_5.html')

def refer_view(request):
    return render(request, 'refer.html')

def home_view(request):
    return render(request, 'home.html')

@login_required
def doc_cover_view(request):
    user = request.user
    action = request.POST.get('action')
    print (action)
    initial = {}

    # 🔹 แยก get_data_cover ออกมา
    if request.method == 'POST' and action == 'get_data_cover':
        try:
            project = DocCover.objects.get(user=user)
            initial = {
            'name_pro_th': project.project_name_th,
            'name_pro_en': project.project_name_en,
            'academic_year': project.academic_year,
            'authors_th': [project.author1_name_th or '', project.author2_name_th or ''],
            'authors_en': [project.author1_name_en or '', project.author2_name_en or ''],
        }

        
            initial['authors_th_json'] = json.dumps(initial.get('authors_th', []))
            initial['authors_en_json'] = json.dumps(initial.get('authors_en', []))

        except DocCover.DoesNotExist:
                initial = {}

        return render(request, 'cover.html', {'initial': initial})

    # 🔹 ส่วนบันทึก / สร้างเอกสาร
    if request.method == 'POST' and action in ['save_cover', 'generate_cover_th','generate_cover_en','generate_cover_sec']:
        project_name_th = request.POST.get('name_pro_th', '')
        project_name_en = request.POST.get('name_pro_en', '')
        author1_th = request.POST.get('name_author_th_1', '')
        author2_th = request.POST.get('name_author_th_2', '')
        author1_en = request.POST.get('name_author_en_1', '')
        author2_en = request.POST.get('name_author_en_2', '')
        academic_year = request.POST.get('academic_year', '')

        # บันทึกหรืออัปเดตข้อมูลหน้าปก
        DocCover.objects.update_or_create(
            user=user,
            defaults={
                'project_name_th': project_name_th,
                'project_name_en': project_name_en,
                'author1_name_th': author1_th,
                'author2_name_th': author2_th,
                'author1_name_en': author1_en,
                'author2_name_en': author2_en,
                'academic_year': academic_year,
            }
        )

        # สร้างไฟล์ .docx ถ้าเลือก generate
        if action == 'generate_cover_th':
            doc = doc_cover_th(project_name_th, project_name_en, author1_th, author2_th, author1_en, author2_en, academic_year)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename=cover_th.docx'
            doc.save(response)
            return response

        elif action == 'generate_cover_en':
            doc = doc_cover_en(project_name_th, project_name_en, author1_th, author2_th, author1_en, author2_en, academic_year)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename=cover_en.docx'
            doc.save(response)
            return response
        elif action == 'generate_cover_sec':
            doc = doc_cover_sec(project_name_th, project_name_en, author1_th, author2_th, author1_en, author2_en, academic_year)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename=cover_sec.docx'
            doc.save(response)
            return response


    return render(request, 'cover.html')


# แบบฟอร์ม ทก.01
@login_required
def sp_project_form_view(request):
    user = request.user
    initial = {}

    if request.method == 'POST':
        action = request.POST.get('action')
        print(">>> ACTION =", action)  # 🧪 ตรวจดูว่า Django รับค่าอะไรจริงๆ
        
        name_pro_th = request.POST.get('name_pro_th', '')
        name_pro_en = request.POST.get('name_pro_en', '')
        case_stu = request.POST.get('case_stu', '')
        term = request.POST.get('term', '')
        school_y = request.POST.get('school_y', '')
        adviser = request.POST.get('adviser', '')
        co_advisor = request.POST.get('co_advisor', '')
        strategic = request.POST.get('strategic', '')
        plan = request.POST.get('plan', '')
        key_result = request.POST.get('key_result', '')
        bg_and_sig_para1 = request.POST.get('bg_and_sig_para1', '')
        bg_and_sig_para2 = request.POST.get('bg_and_sig_para2', '')
        bg_and_sig_para3 = request.POST.get('bg_and_sig_para3', '')
        purpose_1 = request.POST.get('purpose_1', '')
        purpose_2 = request.POST.get('purpose_2', '')
        purpose_3 = request.POST.get('purpose_3', '')
        authors = [
            request.POST.get('name_author_th_1', ''),
            request.POST.get('name_author_th_2', '')
        ]

        # ✅ อ่าน scope
        scope_data = []
        scope_count = int(request.POST.get('scope_count', 1))
        for i in range(1, scope_count + 1):
            main = request.POST.get(f'scope_b_{i}', '').strip()
            sub_count = int(request.POST.get(f'scope_subcount_{i}', 1))
            subs = []
            for j in range(1, sub_count + 1):
                sub = request.POST.get(f'scope_s_{i}_{j}', '').strip()
                if sub:
                    subs.append(sub)
            scope_data.append({'main': main, 'subs': subs})
        
        # 1. ดักกรณี get_data: แค่โหลด ไม่เซฟ/ไม่ update_or_create ใดๆ
        if action == 'get_data':
            try:
                project = SpProject.objects.get(user=user)
                scope_data = project.scope_json or []
                initial['scope_data'] = scope_data

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
                    'scope_data': scope_data,
                }
            except SpProject.DoesNotExist:
                initial = {}
        # if request.path.endswith('/sp_project_form_2/'):
        #     return render(request, 'sp_project_form_2.html', {'initial': initial})
        # else:
        #     return render(request, 'sp_project_form.html', {'initial': initial})
        status_message = {'message': '✅ ดึงข้อมูลสำเร็จแล้ว!', 'type': 'success'}
        if action == 'save':
        # 2. กรณีบันทึกข้อมูล (save) 
            # ------- Save/update DB -------
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
                    'scope_json': json.dumps(scope_data, ensure_ascii=False),
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
                'scope_data': scope_data,
            }
            status_message = {'message': '✅ บันทึกข้อมูลสำเร็จแล้ว!', 'type': 'success'}
        # ----- กรณี generate -----
        elif action == 'generate':
                print("=== GENERATE ACTION ===")
                doc = doc_sp_01(name_pro_th, name_pro_en, authors,
                case_stu, term, school_y,
                adviser, co_advisor,
                strategic, plan, key_result,
                bg_and_sig_para1, bg_and_sig_para2, bg_and_sig_para3,
                purpose_1, purpose_2, purpose_3,scope_data
            )
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename=sp_project_form.docx'
                doc.save(response)
                return response
                
    if request.path.endswith('/sp_project_form_2/'):
        return render(request, 'sp_project_form_2.html', {'initial': initial})
    else:
        return render(request, 'sp_project_form.html', {'initial': initial})
    

@login_required
def intro_view(request):
    user = request.user
    initial = {}
    action = request.POST.get('action')

    if request.method == 'POST':
        # Action: ดึงข้อมูล
        if action == 'get_data_intro':
            try:
                abstract_data = Abstract.objects.get(user=user)
                initial = {
                    'project_name_th': abstract_data.project_name_th,
                    'project_name_en': abstract_data.project_name_en,
                    'major_th': abstract_data.major_th,
                    'major_en': abstract_data.major_en,
                    'advisor_th': abstract_data.advisor_th,
                    'advisor_en': abstract_data.advisor_en,
                    'coadvisor_th': abstract_data.coadvisor_th,
                    'coadvisor_en': abstract_data.coadvisor_en,
                    'academic_year_th': abstract_data.academic_year_th,
                    'academic_year_en': abstract_data.academic_year_en,
                    'abstract_th_para1': abstract_data.abstract_th_para1,
                    'abstract_th_para2': abstract_data.abstract_th_para2,
                    'abstract_en_para1': abstract_data.abstract_en_para1,
                    'abstract_en_para2': abstract_data.abstract_en_para2,
                    'keyword_th': abstract_data.keyword_th,
                    'keyword_en': abstract_data.keyword_en,
                    'acknow_para1': abstract_data.acknow_para1,
                    'acknow_para2': abstract_data.acknow_para2,
                    'acknow_name1': abstract_data.acknow_name1,
                    'acknow_name2': abstract_data.acknow_name2,
                    'author1_th': abstract_data.author1_th,
                    'author1_en': abstract_data.author1_en,
                    'author2_th': abstract_data.author2_th,
                    'author2_en': abstract_data.author2_en,
                    'total_pages': abstract_data.total_pages,   # ✅ เพิ่มจำนวนหน้า
                }
                messages.success(request, 'ดึงข้อมูลเก่าสำเร็จแล้ว')
                return render(request, 'intro.html', {'initial': initial})
            except Abstract.DoesNotExist:
                messages.info(request, 'ไม่พบข้อมูลเก่า')
                return render(request, 'intro.html', {'initial': {}})

        # Action: บันทึกข้อมูล
        elif action == 'save_intro':
            form_data = {
                'project_name_th': request.POST.get('project_name_th', ''),
                'project_name_en': request.POST.get('project_name_en', ''),
                'major_th': request.POST.get('major_th', ''),
                'major_en': request.POST.get('major_en', ''),
                'advisor_th': request.POST.get('advisor_th', ''),
                'advisor_en': request.POST.get('advisor_en', ''),
                'coadvisor_th': request.POST.get('coadvisor_th', ''),
                'coadvisor_en': request.POST.get('coadvisor_en', ''),
                'academic_year_th': request.POST.get('academic_year_th', ''),
                'academic_year_en': request.POST.get('academic_year_en', ''),
                'abstract_th_para1': request.POST.get('abstract_th_para1', ''),
                'abstract_th_para2': request.POST.get('abstract_th_para2', ''),
                'abstract_en_para1': request.POST.get('abstract_en_para1', ''),
                'abstract_en_para2': request.POST.get('abstract_en_para2', ''),
                'keyword_th': request.POST.get('keyword_th', ''),
                'keyword_en': request.POST.get('keyword_en', ''),
                'acknow_para1': request.POST.get('acknow_para1', ''),
                'acknow_para2': request.POST.get('acknow_para2', ''),
                'acknow_name1': request.POST.get('acknow_name1', ''),
                'acknow_name2': request.POST.get('acknow_name2', ''),
                'author1_th': request.POST.get('author1_th', ''),
                'author1_en': request.POST.get('author1_en', ''),
                'author2_th': request.POST.get('author2_th', ''),
                'author2_en': request.POST.get('author2_en', ''),
                'total_pages': request.POST.get('total_pages', None),   # ✅ เก็บจำนวนหน้า
            }
            Abstract.objects.update_or_create(user=user, defaults=form_data)
            messages.success(request, 'บันทึกข้อมูลเรียบร้อยแล้ว')
            return redirect('intro_view')

        # Action: สร้างไฟล์ Word
        elif action == 'generate_intro':
            form_data = {
                'project_name_th': request.POST.get('project_name_th', ''),
                'project_name_en': request.POST.get('project_name_en', ''),
                'major_th': request.POST.get('major_th', ''),
                'major_en': request.POST.get('major_en', ''),
                'advisor_th': request.POST.get('advisor_th', ''),
                'advisor_en': request.POST.get('advisor_en', ''),
                'coadvisor_th': request.POST.get('coadvisor_th', ''),
                'coadvisor_en': request.POST.get('coadvisor_en', ''),
                'academic_year_th': request.POST.get('academic_year_th', ''),
                'academic_year_en': request.POST.get('academic_year_en', ''),
                'abstract_th_para1': request.POST.get('abstract_th_para1', ''),
                'abstract_th_para2': request.POST.get('abstract_th_para2', ''),
                'abstract_en_para1': request.POST.get('abstract_en_para1', ''),
                'abstract_en_para2': request.POST.get('abstract_en_para2', ''),
                'keyword_th': request.POST.get('keyword_th', ''),
                'keyword_en': request.POST.get('keyword_en', ''),
                'acknow_para1': request.POST.get('acknow_para1', ''),
                'acknow_para2': request.POST.get('acknow_para2', ''),
                'acknow_name1': request.POST.get('acknow_name1', ''),
                'acknow_name2': request.POST.get('acknow_name2', ''),
                'author1_th': request.POST.get('author1_th', ''),
                'author1_en': request.POST.get('author1_en', ''),
                'author2_th': request.POST.get('author2_th', ''),
                'author2_en': request.POST.get('author2_en', ''),
                'total_pages': request.POST.get('total_pages', None),   # ✅ ส่งไป doc_intro.py
            }
            doc = doc_intro(form_data)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename=abstract_and_acknow.docx'
            doc.save(response)
            return response
            
    # ถ้าเป็น GET request (เข้าหน้าครั้งแรก)
    # เราจะส่ง initial เป็น dict ว่างเปล่าเสมอ เพื่อให้ฟอร์มขึ้นมาแบบไม่มีข้อมูล
    return render(request, 'intro.html', {'initial': initial})


# ใบรับรอง
@login_required
# ---------- helper: แปลง model -> initial dict ให้ตรงกับ template ----------
def initial_from_cert(cert):
    return {
        'topic'      : cert.topic or '',
        'author1'    : cert.author1 or '',
        'author2'    : cert.author2 or '',
        'dean'       : cert.dean or '',
        'chairman'   : cert.chairman or '',
        'committee1' : cert.committee1 or '',
        'committee2' : cert.committee2 or '',
    }

@login_required
def certificate_view(request):
    user = request.user
    initial = {}
    action = request.POST.get('action', '')

    if request.method == 'POST':

        # ----- 1) ดึงข้อมูลจากฐานข้อมูลมาแสดงในฟอร์ม -----
        if action == 'get_certificate':
            try:
                cert = Certificate.objects.get(user=user)
                initial = initial_from_cert(cert)
                messages.success(request, 'ดึงข้อมูลใบรับรองสำเร็จ')
            except Certificate.DoesNotExist:
                messages.info(request, 'ยังไม่มีข้อมูลใบรับรองสำหรับผู้ใช้นี้')
            return render(request, 'Certificate.html', {'initial': initial})

        # ----- 2) บันทึกข้อมูลลงฐานข้อมูล -----
        elif action == 'save_certificate':
            form_data = {
                'topic'     : (request.POST.get('topic') or '').strip(),
                'author1'   : (request.POST.get('author1') or '').strip(),
                'author2'   : (request.POST.get('author2') or '').strip(),
                'dean'      : (request.POST.get('dean') or '').strip(),
                'chairman'  : (request.POST.get('chairman') or '').strip(),
                'committee1': (request.POST.get('committee1') or '').strip(),
                'committee2': (request.POST.get('committee2') or '').strip(),
            }
            Certificate.objects.update_or_create(user=user, defaults=form_data)
            messages.success(request, 'บันทึกข้อมูลใบรับรองเรียบร้อยแล้ว')
            return redirect('certificate')   # ชื่อ route ตาม urls.py

        # ----- 3) ดาวน์โหลดเอกสาร (.docx) -----
        elif action == 'generate_certificate':
            # 3.1 อ่านจากฟอร์ม
            topic      = (request.POST.get('topic') or '').strip()
            author1    = (request.POST.get('author1') or '').strip()
            author2    = (request.POST.get('author2') or '').strip()
            dean       = (request.POST.get('dean') or '').strip()
            chairman   = (request.POST.get('chairman') or '').strip()
            committee1 = (request.POST.get('committee1') or '').strip()
            committee2 = (request.POST.get('committee2') or '').strip()

            # 3.2 ถ้าฟอร์มว่าง ให้ fallback ไปดึงค่าล่าสุดจากฐานข้อมูล
            if not any([topic, author1, author2, dean, chairman, committee1, committee2]):
                try:
                    cert = Certificate.objects.get(user=user)
                    topic      = cert.topic or ''
                    author1    = cert.author1 or ''
                    author2    = cert.author2 or ''
                    dean       = cert.dean or ''
                    chairman   = cert.chairman or ''
                    committee1 = cert.committee1 or ''
                    committee2 = cert.committee2 or ''
                except Certificate.DoesNotExist:
                    messages.error(request, 'ยังไม่มีข้อมูลสำหรับสร้างเอกสาร โปรดบันทึกหรือกดดึงข้อมูลก่อน')
                    return redirect('certificate')

            # 3.3 สร้างเอกสาร
            try:
                doc = doc_certificate(topic, author1, author2, dean, chairman, committee1, committee2)
            except Exception as e:
                messages.error(request, f'สร้างเอกสารล้มเหลว: {e}')
                return redirect('certificate')

            # 3.4 ส่งไฟล์ให้ดาวน์โหลด แล้วจบการทำงานตรงนี้
            buf = io.BytesIO()
            doc.save(buf)
            buf.seek(0)
            return FileResponse(buf, as_attachment=True, filename='certificate.docx')

    # --- GET: แสดงฟอร์มว่างเสมอ ---
    return render(request, 'certificate.html', {'initial': {}})

# ========== บรรณานุกรม ==========

from django.utils.dateparse import parse_date


@login_required
def refer_view(request):
    # -------------------- helpers (no leading underscore) --------------------
    def format_date_lang(date_s: str, lang: str) -> str:
        """รับ 'YYYY-MM-DD' → คืนสตริงตามภาษา: en=YYYY Mon DD, th=DD Mon YYYY(พ.ศ.)"""
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

    def format_dates_for_doc(refs):
        """แปลงเฉพาะฟิลด์วันที่ที่มาจาก <input type='date'> ก่อนส่งเข้า doc_refer()."""
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

    def collect_references_from_post():
        """อ่านค่าจากฟอร์มทั้งหมด → list[dict] ตามโครงที่ doc_refer ใช้"""
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

    def save_websites_from_refs(user, refs):
        """อัปเดตเฉพาะ Website (ref_type=1) ลงตารางเว็บไซต์ของคุณ"""
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
                user=request.user, ref_no=str(i), defaults=defaults
            )

    def save_books_from_refs(user, refs):
        """
        บันทึก Book (ref_type='2') ลงตาราง doc_ref_book แบบ “ลบของเดิมของ user แล้วสร้างใหม่”
        1 row ต่อ 1 รายการที่ผู้ใช้กรอก (ถ้าเป็นภาษาไทยก็เติมฝั่ง *_th, ภาษาอังกฤษก็เติมฝั่ง *_en)
        """
        # ลบของเก่าก่อน เพื่อให้ข้อมูลใน DB ตรงกับฟอร์มปัจจุบัน 1:1
        RefBook.objects.filter(user=user).delete()
        bulk = []
        for r in refs:
            if r.get('ref_type') != '2':
                continue
            lang = r.get('language', 'th')

            # parse ตัวเลขให้ปลอดภัย
            def _to_int(val):
                try:
                    s = (val or '').strip()
                    return int(s) if s != '' else None
                except Exception:
                    return None

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
            else:  # th
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

    def initial_refs_from_db(user):
        """ดึง Website ของ user → สร้าง list[dict] สำหรับ hydrate ฟอร์ม"""
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
        ดึง Book ของ user → คืนเป็นรายการสำหรับ hydrate ฟอร์ม
        1 row ใน DB อาจให้ 1-2 รายการ (th/en) หากทั้งสองฝั่งมีข้อมูล
        """
        out = []
        for b in RefBook.objects.filter(user=user).order_by('ref_book_id'):
            # TH
            if b.book_title_th or b.book_authors_th or b.book_city_print_th or b.book_publisher_th or b.book_y_print_th is not None or b.book_print_count_th is not None:
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
            if b.book_title_en or b.book_authors_en or b.book_city_print_en or b.book_publisher_en or b.book_y_print_en is not None or b.book_print_count_en is not None:
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
    # -------------------- end helpers --------------------

    if request.method == 'POST':
        action = request.POST.get('action')
        print(">>> ACTION =", action)

        # รวมข้อมูลจากฟอร์มทุกครั้ง (ใช้ทั้ง save / generate / get_data)
        references = collect_references_from_post()

        if action == 'save_refer':
            # เซฟ Website + Book
            save_websites_from_refs(request.user, references)
            save_books_from_refs(request.user, references)

            # ดึงกลับไป hydrate
            initial_refs = initial_refs_from_db(request.user) + initial_books_from_db(request.user)
            ctx = {'initial_refs_json': json.dumps(initial_refs, ensure_ascii=False)}
            messages.success(request, f'บันทึกข้อมูลสำเร็จ {len(initial_refs)} รายการ')
            return render(request, 'refer.html', ctx)

        if action == 'generate_refer':
            # เซฟก่อน → แปลงวันที่ตามภาษา → ส่งเข้า doc_refer
            from man_doc.doc_refer import doc_refer
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
            initial_refs = initial_refs_from_db(request.user) + initial_books_from_db(request.user)
            ctx = {'initial_refs_json': json.dumps(initial_refs, ensure_ascii=False)}
            return render(request, 'refer.html', ctx)

    # GET ครั้งแรก: หน้าเปล่า
    return render(request, 'refer.html')



@login_required
def chapter_1_view(request):
    user = request.user
    initial = {}
    status_message = None

    if request.method == 'POST':
        action = request.POST.get('action')
        print(">>> ACTION =", action)
        if action == 'get_data':
            # 2. ดึงข้อมูลจากฐานข้อมูล
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
                    'hypo_items_json': chapter1_data.hypo_items_json, # <--- แก้ไข
                    'scope_json': chapter1_data.scope_json,             # <--- แก้ไข
                    'para_premise': chapter1_data.para_premise,
                    'premise_json': chapter1_data.premise_json,         # <--- แก้ไข
                    'def_items_json': chapter1_data.def_items_json,     # <--- แก้ไข
                    'benefit_items_json': chapter1_data.benefit_items_json, # <--- แก้ไข
                }
                status_message = {'message': '✅ ดึงข้อมูลสำเร็จแล้ว!', 'type': 'success'}
            except Chapter1.DoesNotExist:
                initial = {}
                status_message = {'message': 'ไม่มีข้อมูลอยู่ กรุณากรอกข้อมูลแล้วบันทึก!', 'type': 'warning'}

        elif action == 'save' or action == 'generate':
            # 1. อ่านข้อมูลล่าสุดจากฟอร์ม (ย้ายมาไว้ตรงนี้)
            sec11_p1 = request.POST.get('sec11_p1', '')
            sec11_p2 = request.POST.get('sec11_p2', '')
            sec11_p3 = request.POST.get('sec11_p3', '')
            
            purpose_count = int(request.POST.get('purpose_count', 0))
            purpose_1 = request.POST.get('purpose_1', '')
            purpose_2 = request.POST.get('purpose_2', '')
            purpose_3 = request.POST.get('purpose_3', '')

            hypo_paragraph = request.POST.get('hypo_paragraph', '')
            hypo_items = json.loads(request.POST.get('hypo_items_json', '[]'))
            scope_data = json.loads(request.POST.get('scope_json', '[]'))
            para_premise_str = request.POST.get('para_premise', '')
            premise_data = json.loads(request.POST.get('premise_json', '[]'))
            def_items = json.loads(request.POST.get('def_items_json', '[]'))
            benefit_items = json.loads(request.POST.get('benefit_items_json', '[]'))
            
            # --- จัดการ Action ---
            if action == 'save':
                # 2. บันทึก/อัปเดตข้อมูลลงฐานข้อมูล (เหมือนเดิม)
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
                # 3. สร้างเอกสาร DOCX จากข้อมูลล่าสุดบนฟอร์ม
                    doc = doc_chapter1(sec11_p1,sec11_p2,sec11_p3,purpose_count,purpose_1,purpose_2,purpose_3,hypo_paragraph,
                hypo_items,scope_data,para_premise_str,premise_data,def_items,benefit_items)
                    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                    response['Content-Disposition'] = 'attachment; filename=chapter1.docx'
                    doc.save(response) 
                    return response
                    
                    
            
           # Get data โดยไม่กดปุ่ม
           # อัปเดต initial เพื่อแสดงผลข้อมูลล่าสุด
            initial = {
                'sec11_p1': sec11_p1,
                'sec11_p2': sec11_p2,
                'sec11_p3': sec11_p3,
                'purpose_count': purpose_count,
                'purpose_1': purpose_1,
                'purpose_2': purpose_2,
                'purpose_3': purpose_3,
                'hypo_paragraph': hypo_paragraph,
                'hypo_items_json': hypo_items,             # <-- แก้ไข
                'scope_json': scope_data,                 # <-- แก้ไข
                'para_premise': para_premise_str,
                'premise_json': premise_data,             # <-- แก้ไข
                'def_items_json': def_items,              # <-- แก้ไข
                'benefit_items_json': benefit_items,      # <-- แก้ไข
            }
    context = {
        'initial': initial,
        'status_message': status_message
    }
        
        # 2. สั่ง render พร้อมส่ง context ไปด้วย (มีแค่จุดเดียวท้ายฟังก์ชัน)
    return render(request, 'chapter_1.html', context)
        
#บท5
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
    """
    ทำ schema กลาง + ใส่ลำดับ order:
      section: {title:str, body:str, mains:[{text:str, subs:[str], main_order:int}], section_order:int}
    """
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
    """
    เรียงตาม order + เติมหมายเลขสำหรับ UI:
      section['no'] = 5.i
      main['no']    = 5.i.j
      sub -> {"text": "...", "no": "5.i.j.k"}
    *เลขนี้เพื่อ UI เท่านั้น ไม่จำเป็นต้องเก็บลง DB*
    """
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

def _render_docx(intro_body: str, sections_sorted: list) -> Document:
    """
    สร้างไฟล์ .docx ตามโครงสร้างที่เรียงและมีเลขแล้ว (สำหรับ export)
    """
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'TH SarabunPSK'
    style.font.size = Pt(16)

    # หัวเรื่องบทที่ 5
    h = doc.add_heading('บทที่ 5', level=1)
    h.style.font.name = 'TH SarabunPSK'
    h.style.font.size = Pt(20)

    # บทนำ (ถ้ามี)
    if intro_body:
        doc.add_heading('บทนำ', level=2)
        doc.add_paragraph(intro_body)

    # เนื้อหา 5.1 … 5.n
    for sec in sections_sorted:
        title = _get_title(sec)
        no = sec.get('no') or ''
        head = f'{no} {title}'.strip()
        if head:
            doc.add_heading(head, level=2)

        body = _get_body(sec)
        if body:
            doc.add_paragraph(body)

        for m in sec.get('mains', []):
            main_text = (m.get('text') or '').strip()
            main_no = m.get('no') or ''
            if main_text or main_no:
                doc.add_paragraph(f'{main_no} {main_text}'.strip())

            for sub in m.get('subs', []):
                sub_no = sub.get('no') or ''
                sub_text = (sub.get('text') or '').strip()
                if sub_text or sub_no:
                    p = doc.add_paragraph(f'{sub_no} {sub_text}'.strip())
                    p.paragraph_format.left_indent = Cm(1)

    return doc

# ---------- helper: แปลง JSON จาก UI → schema สำหรับเอนจินเอกสาร ----------
def _sections_from_ui_json(raw_json: str, fallback_list):
    """
    รับ JSON จากฟอร์ม chapter_5.html (title/body/points[{main,subs[]}])
    คืนค่าสำหรับ _render_docx(): [{title, body, mains:[{text, subs:[]}]}, ...]
    """
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

    # ดึงข้อมูลล่าสุดจาก DB (ใช้ได้ทั้ง GET/POST)
    row = Chapter5.objects.filter(user=user).order_by('-updated_at').first()
    db_intro = (row.intro_th if row else '') or ''
    db_sections = row.sections_json if (row and isinstance(row.sections_json, list)) else []

    def safe_parse_list(raw: str, default: list):
        """พาร์ส JSON จากฟอร์มให้ปลอดภัย; ถ้าเพี้ยน/ไม่ใช่ list ให้คืน default"""
        try:
            data = json.loads(raw or '[]')
            return data if isinstance(data, list) else (default or [])
        except json.JSONDecodeError:
            return default or []

    if request.method == 'POST':
        action = (request.POST.get('action') or '').strip()
        intro_body = (request.POST.get('intro_body') or '').strip()
        raw_json = request.POST.get('chapter5_json', '')

        # ---------- SAVE ----------
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
            messages.success(request, '💾 บันทึกข้อมูลบทที่ 5 เรียบร้อยแล้ว (ฟอร์มถูกเคลียร์)')
            # เคลียร์ฟอร์มตามดีไซน์
            return render(request, 'chapter_5.html', {
                'initial': {'intro_body': '', 'chapter5_json': []}
            })

        # ---------- GET DATA ----------
        elif action == 'get_data':
            messages.info(request, '🔄 ดึงข้อมูลล่าสุดเรียบร้อยแล้ว')
            return render(request, 'chapter_5.html', {
                'initial': {'intro_body': db_intro, 'chapter5_json': db_sections}
            })

        # ---------- GENERATE DOCX ----------
        elif action == 'generate_docx':
            # ใช้ค่าจากฟอร์ม ถ้าไม่มีก็ fallback DB
            sections_for_doc = safe_parse_list(raw_json, db_sections)
            if not intro_body:
                intro_body = db_intro

            # สร้างเอกสารตามคู่มือ
            doc = doc_chapter5(intro_body, sections_for_doc)

            # ส่งไฟล์กลับแล้วจบการทำงานในสาขานี้
            buf = BytesIO()
            doc.save(buf)
            buf.seek(0)
            return FileResponse(
                buf,
                as_attachment=True,
                filename='chapter5.docx',
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

        # ---------- action อื่น ๆ ----------
        messages.info(request, 'ยังไม่รองรับการทำงานนี้')
        return render(request, 'chapter_5.html', {
            'initial': {'intro_body': '', 'chapter5_json': []}
        })

    # ---------- GET: preload ถ้ามีใน DB ----------
    return render(request, 'chapter_5.html', {
        'initial': {
            'intro_body': (db_intro if (db_intro or db_sections) else ''),
            'chapter5_json': (db_sections if isinstance(db_sections, list) else []),
        }
    })
