from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm,LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from man_doc.doc_sp_01 import doc_sp_01  # ←  นำเข้าไฟล์ที่คุณแยกไว้


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


def sp_project_form_view(request):
    if request.method == 'POST':
        name_pro_th = request.POST.get('name_pro_th')
        name_pro_en = request.POST.get('name_pro_en')
        case_stu = request.POST.get('case_stu')
        term = request.POST.get('term')
        school_y = request.POST.get('school_y')
        adviser = request.POST.get('adviser')
        co_advisor = request.POST.get('co_advisor')
        strategic = request.POST.get('strategic')
        plan = request.POST.get('plan')
        key_result = request.POST.get('key_result')
        # เก็บรายชื่อนักศึกษาจาก name_author_th_1, 2, 3,...
        authors = []
        i = 1
        while True:
            key = f'name_author_th_{i}'
            value = request.POST.get(key)
            if value:
                authors.append(value)
                i += 1
            else:
                break

        # ส่ง authors ไปยัง doc_sp_01
        doc = doc_sp_01(name_pro_th, name_pro_en, authors,case_stu,term,school_y,adviser,co_advisor,strategic,plan,key_result)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename=sp_project_form.docx'
        doc.save(response)
        return response

    return render(request, 'sp_project_form.html')

