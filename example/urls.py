# example/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('login/', views.login_user, name='login_user'),
    path('home/', views.home, name='home'),
]