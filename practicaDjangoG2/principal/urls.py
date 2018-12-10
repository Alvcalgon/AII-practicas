from django.urls import path
from django.contrib import admin
from django.urls import re_path
from django.conf import settings
from django.views import static

from principal.views import index
from principal import views

urlpatterns = [
        path('', views.index, name = 'index'),
        path('banco/edit', views.get_banco),
        path('sucursal/edit', views.get_sucursal),
        path('usuario/edit', views.get_usuario),
        path('cuenta/edit', views.get_cuenta),
        path('movimiento/edit', views.get_movimiento),
        path('sucursal/list', views.sucursales),
        path('usuario/list', views.usuarios),
    ]