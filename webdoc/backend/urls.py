# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('manage/', views.manage_doc, name='manage_doc'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
