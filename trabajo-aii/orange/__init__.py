# encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3

# Tarifas para hablar y navegar

def extraer_tarifas_hablar_navegar():
    f = urllib.request.urlopen("https://www.phonehouse.es/tarifas/orange/movil-contrato.html")
    s = BeautifulSoup(f, "lxml")
    l = s.find_all("li", class_=["linea"])
    return l

def cargar_tarifas_hablar_navegar():
    lista_tarifas = []
    
    l = extraer_tarifas_hablar_navegar()
    
    for e in l:
        tag_nombre_tarifa = e.find("div", class_ = ["nombre-tarifa"])

        #tag_titulo_tabla = e.find_all("div", class_ = ["datos"])
        #for i in tag_titulo_tabla:
            #tag_titulo = i.find("div", class_ = ["titulo"])
            #titulo = tag_titulo.string.strip()
            
        tag_div_minutos_tarifa = e.find_all("div", class_ = ["col_2"])
        for i in tag_div_minutos_tarifa:
            tag_minutos_tarifa = i.find("ul")
            #tag_minutos_tarifa = i.find("ul")
            minutos_tarifa = tag_minutos_tarifa.string
            if(minutos_tarifa == None):
                minutos_tarifa = tag_minutos_tarifa
                
         
        tag_div_internet_tarifa = e.find_all("div", class_ = ["col_3"])
        for j in tag_div_internet_tarifa:
            tag_internet_tarifa = j.find("li")
            internet_tarifa = tag_internet_tarifa.string.strip()
         
        tag_ul_promocion_tarifa = e.find_all("ul", class_= ["promo"])
        for z in tag_ul_promocion_tarifa:
            tag_promocion_tarifa = z.find("li")
            promocion_tarifa = tag_promocion_tarifa.string.strip()
             
        tag_div_precio_tarifa = e.find_all("div", class_ = ["precio"])
        for a in tag_div_precio_tarifa:
            tag_precio_tarifa = a.find("strong")
            precio_tarifa = tag_precio_tarifa.string.strip()
             
             
             
        nombre_tarifa = tag_nombre_tarifa.string.strip()
         
        precio_tarifa = tag_precio_tarifa.string.strip()
         
        if(nombre_tarifa == None):
            nombre_tarifa = ""
        elif (minutos_tarifa == None):
            minutos_tarifa = ""
        elif (internet_tarifa == None):
            internet_tarifa = ""
        elif (promocion_tarifa == None):
            promocion_tarifa = ""
        elif(precio_tarifa == None):
            precio_tarifa = ""    
            
        
        
        tarifa = [nombre_tarifa, minutos_tarifa, internet_tarifa, promocion_tarifa, precio_tarifa+' €']
        #tarifa = [nombre_tarifa]
        lista_tarifas.append(tarifa)
        
        
    return (lista_tarifas)
    
    
#print(cargar_tarifas_hablar_navegar())

# Tarifas ADSL o Fibra

def extraer_adsl_fibra():
    f = urllib.request.urlopen("https://www.phonehouse.es/tarifas/orange/adsl-fibra.html")
    s = BeautifulSoup(f, "lxml")
    l = s.find_all("li", class_=["linea"])
    return l

def cargar_adsl_fibra():
    lista_tarifas = []
    
    l = extraer_adsl_fibra()
    
    for e in l:
        tag_nombre_tarifa = e.find("div", class_ = ["nombre-tarifa"])
        tag_velocidad_adsl = e.find("h4")
        
        tag_div_fijo = e.find("div", class_ = ["col_3"])
        tag_fijo = tag_div_fijo.find_all("li")
        for i in tag_fijo:
            fijo = i.string.strip()
        
        tag_ul_promo = e.find("ul", class_ = ["promo"])
        tag_promo = tag_ul_promo.find("li")
        tag_div_precio = e.find("strong")
        
        nombre_tarifa = tag_nombre_tarifa.string.strip()
        velocidad_adsl = tag_velocidad_adsl.string.strip()
        promo = tag_promo.string.strip()
        precio = tag_div_precio.string.strip()
        
        tarifa = [nombre_tarifa, velocidad_adsl+ ' ADSL', fijo, promo, precio+' €']
        
        lista_tarifas.append(tarifa)
        
    return (lista_tarifas)

print(cargar_adsl_fibra())
        
        
                
    