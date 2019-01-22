from django.shortcuts import render
from principal.models import Operadora, Tarifa_movil,ADSL_FIBRA,Paquete
from principal.populateDB import populateDatabase
from principal import whooshGoodPack

# Create your views here.

def index(request): 
    return render(request, 'principal/index.html')

def populateDB(request):
    populateDatabase()
    return render(request, 'populateDB.html')

def paquetes(request):
    paquetes=Paquete.objects.all()
    return render(request,'paquetes.html', {'paquetes':paquetes})

def tarifaMovil(request):
    tarifas=Tarifa_movil.objects.all()
    return render(request,'tarifaMovil.html',{'tarifas':tarifas})

def internet(request):
    internets=ADSL_FIBRA.objects.all()
    return render(request,'internet.html',{'internets':internets})

def info(request):
    info=Operadora.objects.all()
    return render(request,'info.html',{'info':info})

def indexar(request):
    whooshGoodPack.indexar()
    return render(request, 'indexar.html')


    