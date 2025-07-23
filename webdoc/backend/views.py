from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm,LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from man_doc.doc_sp_01 import doc_sp_01  # ←  นำเข้าไฟล์ที่คุณแยกไว้
from man_doc.doc_cover import doc_cover_th  # ←  นำเข้าไฟล์ที่คุณแยกไว้
from .models import SpProject, SpProjectAuthor
from django.http import HttpResponse

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
    return render(request, 'index.html')  

def manage_doc(request):
    return render(request, 'index.html')  

def about(request):
    return render(request, 'index.html')  

def cover_view(request):
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


def doc_cover_th_view(request):
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

        if action == 'generate':
                doc = doc_sp_01(
                    name_pro_th, name_pro_en, authors,
                    case_stu, term, school_y,
                    adviser, co_advisor,
                    strategic, plan, key_result
                )
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = 'attachment; filename=sp_project_form.docx'
                doc.save(response)
                return response

        elif action == 'save' or action == 'generate':
            # ดึงข้อมูลจาก POST
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

            # บันทึกลง DB
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

            # อัปเดตชื่อผู้จัดทำ
            SpProjectAuthor.objects.filter(userid=user.user_id, project=project).delete()
            for name in authors:
                SpProjectAuthor.objects.create(
                    userid=user.user_id,
                    name=name,
                    project=project
                )

            # สร้าง docx ถ้าผู้ใช้กด generate
            if action == 'generate':
                doc = doc_sp_01(
                    name_pro_th, name_pro_en, authors,
                    case_stu, term, school_y,
                    adviser, co_advisor,
                    strategic, plan, key_result
                )
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = 'attachment; filename=sp_project_form.docx'
                doc.save(response)
                return response

        

    return render(request, 'sp_project_form.html', {'initial': initial})