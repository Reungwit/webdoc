# urls.py
from django.urls import path
from . import views
from .views import doc_cover_view

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('index', views.index, name='index'),
    path('manage/', views.manage_doc, name='manage_doc'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('cover/', views.doc_cover_view, name='cover'),
    path('sp_project_form/', views.sp_project_form_view, name='sp_project_form'),
    path('sp_project_form_2/', views.sp_project_form_view, name='sp_project_form_2'),
    path('intro/', views.intro_view, name='intro'),
    path('chapter_1/', views.chapter_1_view, name='chapter_1'),
    path('chapter_2/', views.chapter_2_view, name='chapter_2'),
    path('chapter_3/', views.chapter_3_view, name='chapter_3'),
    path('chapter_4/', views.chapter_4_view, name='chapter_4'),
    path('chapter_5/', views.chapter_5_view, name='chapter_5'),
    path('refer/', views.refer_view, name='refer'),


    
]
