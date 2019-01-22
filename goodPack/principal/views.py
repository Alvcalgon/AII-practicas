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
    return render(request,'tarifaMovil.html')

def internet(request):
    return render(request,'internet.html')

def info(request):
    info=Operadora.objects.all()
    return render(request,'info.html',{'info':info})

def indexar(request):
    whooshGoodPack.indexar()
    return render(request, 'indexar.html')

def buscar_tarifa(request):
    if request.method=='GET':
        form = tarifaForm(request.GET, request.FILES)
        if form.is_valid():
            tarifaId = form.cleaned_data['search']
            
            return render(request,'tarifaMovil.html', {'tarifaId':tarifaId})
    form=tarifaForm()
    return render(request,'search_user.html', {'form':form })   
    
    
    
    