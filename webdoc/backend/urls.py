from django.urls import path
from . import views

app_name = 'webdoc'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('manage/', views.manage_doc, name='manage_doc'),
    path('about/', views.about, name='about'),
    path('template/<str:slug>/', views.section_detail, name='section_detail'),

]

