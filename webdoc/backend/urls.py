from django.urls import path
from . import views

app_name = 'webdoc'  # กำหนด namespace

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('index/', views.index_view, name='index'),
    path('manage/', views.manage_doc, name='manage_doc'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    # แก้ตรงนี้: ใช้ <str:slug> แทน <slug:slug> เพื่อรองรับภาษาไทย
    path('template/<str:slug>/', views.section_detail, name='section_detail'),
]
