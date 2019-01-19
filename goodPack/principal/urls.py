from django.urls import path

from principal import views

urlpatterns = [
    # ex: principal/
    path('', views.index, name = 'index'),
    path('populateDB/', views.populateDB, name = 'populate'),
]