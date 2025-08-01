from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from .models import SpProject, SpProjectAuthor, DocCover
from man_doc.doc_sp_01 import doc_sp_01
from man_doc.doc_cover import doc_cover_th, doc_cover_en, doc_cover_sec  # <-- ถ้ามี doc_cover_en ต้อง import ด้วย
from .models import Abstract
from django.http import HttpResponse
import json
from django.shortcuts import render
# Register / Login / Logout
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
            return redirect('webdoc:index')  # ใส่ namespace
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# Static Pages

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

def chapter_5_view(request):
    return render(request, 'chapter_5.html')

def refer_view(request):
    return render(request, 'chapter_5.html')


@login_required
def doc_cover_view(request):
    user = request.user
    action = request.POST.get('action')
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

        # ✅ เยื้องตรงระดับกับ initial
            initial['authors_th_json'] = json.dumps(initial.get('authors_th', []))
            initial['authors_en_json'] = json.dumps(initial.get('authors_en', []))

        except DocCover.DoesNotExist:
                initial = {}

        return render(request, 'cover.html', {'initial': initial})

    # 🔹 ส่วนบันทึก / สร้างเอกสาร
    if request.method == 'POST' and action in ['save_cover', 'generate_cover_th']:
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

def sp_project_form_view(request):
    user = request.user
    initial = {}

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
                }

                authors = list(
                    SpProjectAuthor.objects.filter(userid=user.user_id, project=project)
                    .values_list('name', flat=True)
                )
                initial['authors'] = authors
            except SpProject.DoesNotExist:
                initial = {}

<<<<<<< Updated upstream
        elif action in ['save', 'generate']:
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

            authors = [
                request.POST.get(f'name_author_th_{i}', '')
                for i in range(1, 4)
                if request.POST.get(f'name_author_th_{i}', '')
            ]

            # บันทึกลงฐานข้อมูล
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
                    'key_result': key_result
                }
            )

            # ลบแล้วบันทึกชื่อผู้จัดทำใหม่
            SpProjectAuthor.objects.filter(userid=user.user_id, project=project).delete()
            for name in authors:
                SpProjectAuthor.objects.create(userid=user.user_id, name=name, project=project)

            # สร้างเอกสาร docx
            if action == 'generate':
                doc = doc_sp_01(
                    name_pro_th, name_pro_en, authors,
                    case_stu, term, school_y,
                    adviser, co_advisor,
                    strategic, plan, key_result
                )
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename=sp_project_form.docx'
                doc.save(response)
                return response

    return render(request, 'sp_project_form.html', {'initial': initial})
=======
        if request.path.endswith('/sp_project_form_2/'):
            return render(request, 'sp_project_form_2.html', {'initial': initial})
        else:
            return render(request, 'sp_project_form.html', {'initial': initial})
        
#ของบทคัดย่อ

def intro_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # if 'fetch' in request.POST:
        #     # กรณีดึงข้อมูลล่าสุด
        #     try:
        #         latest_data = Abstract.objects.latest('abstract_id')
        #         return render(request, 'intro.html', {
        #             'abstract': latest_data,
        #             'success_message': 'ดึงข้อมูลล่าสุดสำเร็จ'
        #         })
        #     except Abstract.DoesNotExist:
        #         return render(request, 'intro.html', {
        #             'error_message': 'ยังไม่มีข้อมูลในระบบ'
        #         })

        if action == 'save_intro':
            try:
                # ฟังก์ชันแปลงค่าเป็น int อย่างปลอดภัย
                def safe_int(val, default=0):
                    try:
                        return int(val)
                    except (TypeError, ValueError):
                        return default

                # ดึงค่า abstract_id (ถ้ามี) เพื่อระบุว่าบันทึกใหม่หรืออัปเดต
                abstract_id = request.POST.get('abstract_id')
                if abstract_id:
                    lookup = {'abstract_id': abstract_id}
                else:
                    project_name_th = request.POST.get('project_name_th', '').strip()
                    academic_year_th = request.POST.get('academic_year_th', '').strip()
                    if not project_name_th or not academic_year_th.isdigit():
                        return render(request, 'intro.html', {'error_message': 'กรุณากรอกชื่อโปรเจคและปีการศึกษาให้ถูกต้อง'})
                    lookup = {
                        'project_name_th': project_name_th,
                        'academic_year_th': int(academic_year_th),
                    }

                # ใช้ update_or_create บันทึกหรืออัปเดตข้อมูลบทคัดย่อ
                obj, created = Abstract.objects.update_or_create(
                    defaults={
                        'author1_th': request.POST.get('author1_th', ''),
                        'author1_en': request.POST.get('author1_en', ''),
                        'author2_th': request.POST.get('author2_th', ''),
                        'author2_en': request.POST.get('author2_en', ''),
                        'project_name_en': request.POST.get('project_name_en', ''),
                        'abstract_th': request.POST.get('abstract_th', ''),
                        'abstract_en': request.POST.get('abstract_en', ''),
                        'major_th': request.POST.get('major_th', ''),
                        'major_en': request.POST.get('major_en', ''),
                        'advisor_th': request.POST.get('advisor_th', ''),
                        'advisor_en': request.POST.get('advisor_en', ''),
                        'coadvisor_th': request.POST.get('coadvisor_th', ''),
                        'coadvisor_en': request.POST.get('coadvisor_en', ''),
                        'academic_year_en': safe_int(request.POST.get('academic_year_en')),
                        'keyword_th': request.POST.get('keyword_th', ''),
                        'keyword_en': request.POST.get('keyword_en', ''),
                    },
                    **lookup
                )
                msg = 'สร้างข้อมูลใหม่' if created else 'อัปเดตข้อมูลเรียบร้อยแล้ว'
                return render(request, 'intro.html', {'success_message': msg, 'abstract': obj})

            except Exception as e:
                return render(request, 'intro.html', {'error_message': f'เกิดข้อผิดพลาด: {e}'})

    # กรณี GET หรือ method อื่นๆ
    return render(request, 'intro.html')
>>>>>>> Stashed changes
