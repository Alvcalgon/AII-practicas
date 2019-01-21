from django.urls import path

from principal import views

urlpatterns = [
    # ex: principal/
    path('', views.index, name = 'index'),
    path('populateDB', views.populateDB, name = 'populate'),
    path('paquetes',views.paquetes,name='paquetes'),
    path('tarifaMovil',views.tarifaMovil,name='tarifaMovil'),
    path('internet',views.internet,name='internet'),
    path('info',views.info,name='info')
]