"""resume_parser.parser_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('resumes/', views.resumes_list, name='resumes_list'),
    path('resume/delete/<int:pk>/', views.delete_resume, name='delete_resume'),
    path('resume/update/<int:pk>/', views.update_resume, name='update_resume'),
    path('resumes/export/', views.export_resumes, name='export_resumes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
