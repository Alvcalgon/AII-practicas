from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Max
from principal.models import Sucursales, Movimientos

# Create your views here.
def index(request):
    return HttpResponse("Esta es la pagina indice de la app Principal.")


def sucursales(request,id_banco):
    sucursales=Sucursales.objects.all(Sucursales,fk_banco=id_banco)
    
    return render(request,'sucursales.html', {'datos':sucursales,'MEDIA_URL': settings.MEDIA_URL})


def usuarios(request):
    usuario=Movimientos.objects.all().aggregate(Max('euros'))
    
    return render(request,'usuarios.html', {'datos':usuario,'MEDIA_URL': settings.MEDIA_URL})


def usuarios(request):
    usuario=Movimientos.objects.filter(Sucursales=fk_banco).order_by('-euros')[:2]
    
    return render(request,'usuarios.html', {'datos':usuario,'MEDIA_URL': settings.MEDIA_URL})