from django.shortcuts import render

from principal.populateDB import populateDatabase

# Create your views here.

def index(request):
    return render(request, 'principal/index.html')

def populateDB(request):
    populateDatabase()
    return render(request, 'principal/index.html')