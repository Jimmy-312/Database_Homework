"""django_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from query.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('query_patient/',query_patient),
    path('query_detail/',query_detail),
    path('query_adetail/',query_adetail),
    path('main/',mainpage),
    path('patient_add/',patient_add),
    path('logout/',logout_d),
    path('get_patient/',get_patient),
    path('del_patient/',del_patient),
    path('detail_add/',detail_add),
    path('adetail_add/',adetail_add),
    path('get_detail/',get_detail),
    path('get_adetail/',get_adetail),
    path('detail_del/',detail_del),
    path('adetail_del/',adetail_del),
    path('get_hos/',get_hos),
    path('get_doc/',get_doc),
    path('getUser/',getuser),
    path('edit_user/',edituser),
    path('edit_pass/',editpass),
]
