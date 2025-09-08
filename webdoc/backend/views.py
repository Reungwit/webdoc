from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .forms import RegisterForm, LoginForm
from .models import SpProject, SpProjectAuthor, DocCover, Abstract , Certificate ,Chapter1
from man_doc.doc_sp_01 import doc_sp_01
from man_doc.doc_cover import doc_cover_th, doc_cover_en, doc_cover_sec  
from man_doc.doc_intro import doc_intro  
from man_doc.doc_refer import doc_refer  
from django.template.loader import render_to_string
from man_doc.doc_chapter1 import doc_chapter1
from .models import RefWebsite, RefBook
from django.utils.dateparse import parse_date
import io
from django.http import FileResponse
from man_doc.doc_certificate import doc_certificate


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
                        SpProjectAuthor.objects.filter(userid=user.user_id, project=project)
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
            SpProjectAuthor.objects.filter(userid=user.user_id, project=project).delete()
            for name in authors:
                SpProjectAuthor.objects.create(userid=user.user_id, name=name, project=project)

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
def _initial_from_cert(cert):
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
                initial = _initial_from_cert(cert)
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
@login_required
@csrf_exempt
def refer_view(request):
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action', '')

        # ---------- A) SAVE ----------
        if action == 'save_refer':
            try:
                ref_count = int(request.POST.get('ref_count', 0))
            except (TypeError, ValueError):
                ref_count = 0

            saved = 0
            for i in range(1, ref_count + 1):
                ref_type = request.POST.get(f'ref_type_{i}', '')
                lang = request.POST.get(f'lang_{i}', 'th')

                # รวม author
                authors = []
                for j in range(1, 4):
                    a = (request.POST.get(f'author_{i}_{j}', '') or '').strip()
                    if a:
                        authors.append(a)

                if ref_type == '1':  # Website
                    title = (request.POST.get(f'title_{i}', '') or '').strip()
                    url = (request.POST.get(f'url_{i}', '') or '').strip()
                    acc_raw = (request.POST.get(f'access_date_{i}', '') or '').strip()
                    acc_date = parse_date(acc_raw) if acc_raw else None

                    if title and url:
                        RefWebsite.objects.create(
                            user=user,
                            number=i,  # ✅ เก็บลำดับ
                            title_th=title if lang == 'th' else '',
                            title_en=title if lang == 'en' else '',
                            authors_th_json=authors if lang == 'th' else [],
                            authors_en_json=authors if lang == 'en' else [],
                            url=url,
                            accessed_date=acc_date,
                        )
                        saved += 1

                elif ref_type == '2':  # Book
                    title = (request.POST.get(f'title_{i}', '') or '').strip()
                    print_count = (request.POST.get(f'print_count_{i}', '') or '').strip()
                    city_print = (request.POST.get(f'city_print_{i}', '') or '').strip()
                    publisher = (request.POST.get(f'publisher_{i}', '') or '').strip()
                    y_print = (request.POST.get(f'y_print_{i}', '') or '').strip()
                    year = int(y_print) if y_print.isdigit() else None

                    if title:
                        RefBook.objects.create(
                            user=user,
                            number=i,  # ✅ เก็บลำดับ
                            title_th=title if lang == 'th' else '',
                            title_en=title if lang == 'en' else '',
                            edition_th=print_count if lang == 'th' else '',
                            edition_en=print_count if lang == 'en' else '',
                            publisher_place_th=city_print if lang == 'th' else '',
                            publisher_place_en=city_print if lang == 'en' else '',
                            publisher_th=publisher if lang == 'th' else '',
                            publisher_en=publisher if lang == 'en' else '',
                            year=year,
                            authors_th_json=authors if lang == 'th' else [],
                            authors_en_json=authors if lang == 'en' else [],
                        )
                        saved += 1

            messages.success(request, f'✅ บันทึกข้อมูล {saved} รายการ')
            return redirect('refer')

        # ---------- B) GET DATA ----------
        elif action == 'get_data':
            initial_refs = []

            # Website
            for r in RefWebsite.objects.filter(user=user).order_by('number', 'id'):
                if r.title_th or (r.authors_th_json or []):
                    language = 'th'
                    authors = r.authors_th_json or []
                    title = r.title_th or ''
                else:
                    language = 'en'
                    authors = r.authors_en_json or []
                    title = r.title_en or ''
                initial_refs.append({
                    'ref_type': '1',
                    'language': language,
                    'authors': authors,
                    'title': title,
                    'url': r.url or '',
                    'access_date': r.accessed_date.isoformat() if r.accessed_date else ''
                })

            # Book
            for r in RefBook.objects.filter(user=user).order_by('number', 'id'):
                if r.title_th or (r.authors_th_json or []):
                    language = 'th'
                    authors = r.authors_th_json or []
                    title = r.title_th or ''
                    print_count = r.edition_th or ''
                    city_print = r.publisher_place_th or ''
                    publisher = r.publisher_th or ''
                else:
                    language = 'en'
                    authors = r.authors_en_json or []
                    title = r.title_en or ''
                    print_count = r.edition_en or ''
                    city_print = r.publisher_place_en or ''
                    publisher = r.publisher_en or ''
                initial_refs.append({
                    'ref_type': '2',
                    'language': language,
                    'authors': authors,
                    'title': title,
                    'print_count': print_count,
                    'city_print': city_print,
                    'publisher': publisher,
                    'y_print': str(r.year or ''),
                })

            return render(
                request,
                'refer.html',
                {'initial_refs_json': json.dumps(initial_refs, ensure_ascii=False)}
            )

        # ---------- C) GENERATE DOCX ----------
        elif action == 'generate_refer':
            references = []

            # ดึง Website
            for r in RefWebsite.objects.filter(user=user).order_by('number', 'id'):
                lang = 'th' if (r.title_th or (r.authors_th_json or [])) else 'en'
                references.append({
                    'ref_count': len(references) + 1,
                    'ref_type': '1',
                    'language': lang,
                    'authors': r.authors_th_json if lang == 'th' else (r.authors_en_json or []),
                    'title': r.title_th if lang == 'th' else r.title_en,
                    'url': r.url or '',
                    'access_date': r.accessed_date.isoformat() if r.accessed_date else ''
                })

            # ดึง Book
            for r in RefBook.objects.filter(user=user).order_by('number', 'id'):
                lang = 'th' if (r.title_th or (r.authors_th_json or [])) else 'en'
                references.append({
                    'ref_count': len(references) + 1,
                    'ref_type': '2',
                    'language': lang,
                    'authors': r.authors_th_json if lang == 'th' else (r.authors_en_json or []),
                    'title': r.title_th if lang == 'th' else r.title_en,
                    'print_count': (r.edition_th if lang == 'th' else r.edition_en) or '',
                    'city_print': (r.publisher_place_th if lang == 'th' else r.publisher_place_en) or '',
                    'publisher': (r.publisher_th if lang == 'th' else r.publisher_en) or '',
                    'y_print': str(r.year or ''),
                })

            doc = doc_refer(references)
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = 'attachment; filename=refer.docx'
            doc.save(response)
            return response

    # ---------- GET ----------
    return render(request, 'refer.html', {'initial_refs_json': 'null'})
        
       