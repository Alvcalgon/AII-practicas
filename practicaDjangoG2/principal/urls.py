from django.urls import path

from . import views
from principal import views
from django.contrib import admin
from django.urls import re_path
from django.conf import settings
from django.views import static

urlpatterns = [
        path('', views.index, name = 'index'),
        path('form/',views.form),
        path('sucursales/', views.sucursales),
        path('usuarios/', views.usuarios),
        path('formMov/', views.formMov)
    ]