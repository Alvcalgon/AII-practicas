from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.db.models import Max

from principal.models import Sucursal, Movimiento
from principal.forms import BancoForm, SucursalForm, UsuarioForm, CuentaForm, MovimientoForm

# Create your views here.
def index(request):
    return HttpResponse("Esta es la pagina indice de la app Principal.")


def sucursales(request):
    sucursales= Sucursal.objects.order_by('banco')
    
    return render(request, 'sucursales.html', {'datos':sucursales,'MEDIA_URL': settings.MEDIA_URL})


def usuarios(request):
    usuario= Movimiento.objects.all().aggregate(Max('euros'))
    
    return render(request,'usuarios.html', {'datos':usuario,'MEDIA_URL': settings.MEDIA_URL})

"""
def usuarios(request):
    usuario = Movimiento.objects.filter(Sucursales=fk_banco).order_by('-euros')[:2]
    
    return render(request,'usuarios.html', {'datos':usuario,'MEDIA_URL': settings.MEDIA_URL})
"""

# Formularios -------------------------------------------------------

def get_banco(request):
    if request.method == 'POST':
        form = BancoForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/inicio')
    else:
        form = BancoForm()

    return render(request, 'form_banco.html', {'form': form})


def get_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/inicio')
    else:
        form = SucursalForm()

    return render(request, 'form_sucursal.html', {'form': form})


def get_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/inicio')
    else:
        form = UsuarioForm()

    return render(request, 'form_usuario.html', {'form': form})


def get_cuenta(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/inicio')
    else:
        form = CuentaForm()

    return render(request, 'form_cuenta.html', {'form': form})


def get_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/inicio')
    else:
        form = MovimientoForm()

    return render(request, 'form_movimiento.html', {'form': form})

