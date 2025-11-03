from django.urls import path
from . import views
from man_views import *
urlpatterns = [
    path('project-setup/', views.project_setup_view, name='project_setup'),
    path('manage-doc/', views.manage_doc_view, name='manage_doc'),
    path('index/', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),   
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('sp_project_form/', views.sp_project_form_view, name='sp_project_form'),
    path('sp_project_form_2/', views.sp_project_form_view, name='sp_project_form_2'),
    path('abstract_ack/', views.abstract_ack_view, name='abstract_ack_view'),
    path('chapter_1/', views.chapter_1_view, name='chapter_1'),
    path('chapter_2/', views.chapter_2_view, name='chapter_2'),
    path('chapter_3/', views.chapter_3_view, name='chapter_3'),
    path('chapter_4/', views.chapter_4_view, name='chapter_4'),
    path('chapter_5/', views.chapter_5_view, name='chapter_5'),
    path('refer/', views.refer_view, name='refer'),
    path('', views.home_view, name='home'),
    # ใบรับรองปริญญานิพนธ์
    path('certificate/', views.certificate_view, name='certificate'),
    path('legal/terms/', views.terms_view, name='terms'),
    path('legal/privacy/', views.privacy_view, name='privacy'),
    

    
]

