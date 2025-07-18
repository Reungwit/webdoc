from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required

# ข้อมูลตัวอย่าง sections (ถ้าใช้ในหน้า index)
sections = [
    {'slug': 'ทก01', 'name': 'ทก.01'},
    {'slug': 'บทที่1', 'name': 'บทที่ 1'},
    {'slug': 'บทที่2', 'name': 'บทที่ 2'},
]

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('webdoc:login')  # แก้ให้ใส่ namespace
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
    return redirect('webdoc:login')  # ใส่ namespace

@login_required
def index_view(request):
    # ส่งข้อมูล sections ไปให้ template ถ้าต้องการ
    return render(request, 'index.html', {'sections': sections})

@login_required
def manage_doc(request):
    return render(request, 'manage_doc.html')  # แยก template ตามหน้าที่

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def section_detail(request, slug):
    # หา section_name จาก slug
    section_name = next((s['name'] for s in sections if s['slug'] == slug), "ไม่พบส่วนนี้")
    context = {'section_name': section_name}
    return render(request, 'section_detail.html', context)