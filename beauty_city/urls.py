"""beauty_city URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from bc_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='start_page'),
    path('notes/', views.notes, name='notes'),
    path('service/', views.service, name='service'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('service_finally/', views.service_finally, name='service_finally'),
    path('exit/', views.exit, name='exit')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)