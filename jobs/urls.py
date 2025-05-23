"""
URL configuration for job_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('register/',views.register,name='register'),
    path('/',auth_views.LogoutView.as_view(template_name='registration/logout.html'),name='logout'),

    path('joblist/', views.job_list, name="joblist"),
    path('add/', views.create_job, name='create_job'),
    path('job/<int:pk>/edit/', views.update_job, name='update_job'),
    path('job/<int:job_id>/reflect-delete/', views.reflect_and_delete, name='reflect_and_delete'),
    path('reflections/', views.reflection_list, name='reflection_list'),
    path('resumes/', views.resume_list_upload, name='resume_list'),
    path('resume/delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
]

