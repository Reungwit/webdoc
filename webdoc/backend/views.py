from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('./templates/login.html')  # เปลี่ยนชื่อเส้นทางตามต้องการ
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # เปลี่ยนจาก 'home' เป็น 'index'
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

<<<<<<< Updated upstream
from django.contrib.auth.decorators import login_required
=======
def index(request):
    return render(request, './index.html')  # หรือชื่อ template ที่คุณใช้

def manage_doc(request):
    return render(request, './index.html')  # หรือชื่อ template ที่คุณใช้

def about(request):
    return render(request, 'index.html')  # หรือชื่อ template ที่คุณใช้
>>>>>>> Stashed changes

@login_required
def index_view(request):
    return render(request, 'index.html')
