# encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3

# Tarifas para hablar y navegar

def extraer_tarifas_hablar_navegar():
    f = urllib.request.urlopen("https://www.phonehouse.es/tarifas/vodafone/movil-contrato.html")
    s = BeautifulSoup(f, "lxml")
    l = s.find_all("li", class_=["linea"])
    return l

def cargar_tarifas_hablar_navegar():
    lista_tarifas = []
    
    l = extraer_tarifas_hablar_navegar()
    
    for e in l:
        tag_nombre_tarifa = e.find("div", class_ = ["nombre-tarifa"])

            
        tag_div_minutos_tarifa = e.find("div", class_ = ["col_2"])
        tag_minutos_tarifa = tag_div_minutos_tarifa.find("ul")
                
         
        tag_div_internet_tarifa = e.find("div", class_ = ["col_3"])
        tag_internet_tarifa = tag_div_internet_tarifa.find("li")
         
        tag_ul_promocion_tarifa = e.find("ul", class_= ["promo"])
        promocion_tarifa = tag_ul_promocion_tarifa.find("li")
        
             
        tag_div_precio_tarifa = e.find("div", class_ = ["precio"])
        tag_precio_tarifa = tag_div_precio_tarifa.find("strong")
        precio_tarifa = tag_precio_tarifa.string.strip()
             
             
             
        nombre_tarifa = tag_nombre_tarifa.string.strip()
        
        minutos_tarifa = tag_minutos_tarifa.string
        
        internet_tarifa = tag_internet_tarifa.string.strip()
        
        precio_tarifa = tag_precio_tarifa.string.strip()
         
    
        if (minutos_tarifa == None):
            minutos_tarifa = tag_minutos_tarifa.find(string = re.compile(""))
        elif (promocion_tarifa == None):
            promocion_tarifa = "Sin promoción"
        elif(promocion_tarifa != None):
            promocion_tarifa=promocion_tarifa.find(string = re.compile("li")) 
            
        
        
        tarifa = [nombre_tarifa, minutos_tarifa, internet_tarifa, promocion_tarifa, precio_tarifa+' €']
    
        lista_tarifas.append(tarifa)
        
        
    return (lista_tarifas)
    
    
#print(cargar_tarifas_hablar_navegar())

# Tarifas ADSL o Fibra

def extraer_adsl_fibra():
    f = urllib.request.urlopen("https://www.phonehouse.es/tarifas/vodafone/adsl-fibra.html")
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
        tag_ul_fijo = tag_div_fijo.find("ul")
        tag_fijo = tag_ul_fijo.find("li")
        fijo = tag_fijo
        tag_nacionales = tag_ul_fijo.find_all("li")
        for i in tag_nacionales:
            tag_nacionales = i.string.strip()
        
        #for i in tag_fijo:
            #fijo = i.string.strip()
        
        tag_ul_promo = e.find("ul", class_ = ["promo"])
        promo = tag_ul_promo.find("li")
        tag_div_precio = e.find("strong")
        
        nombre_tarifa = tag_nombre_tarifa.string.strip()
        velocidad_adsl = tag_velocidad_adsl.string.strip()
        fijo =  tag_nacionales
        precio = tag_div_precio.string.strip()
        
        if (promo == None):
            promo = "Sin promoción"
        
        tarifa = [nombre_tarifa, velocidad_adsl+ ' ADSL', fijo, promo, precio+' €']
        
        lista_tarifas.append(tarifa)
        
    return (lista_tarifas)

#print(cargar_adsl_fibra())

# Tarifas Fibra + Movil + TV

def extraer_paquetes():
    f = urllib.request.urlopen("https://www.phonehouse.es/tarifas/vodafone/one.html")
    s = BeautifulSoup(f, "lxml")
    l = s.find_all("li", class_=["linea"])
    return l

def cargar_paquetes():
    lista_paquetes = []
    
    paginas = seleccionar_pagina()
    print("Paginas de paquetes", len(paginas))
    for pagina in paginas:
        print(pagina)
        documento = procesar_pagina(pagina)
        l = documento.find_all("li", class_=["linea"])
        for e in l:
            tag_nombre_tarifa = e.find("div", class_ = ["nombre-tarifa"])
            tag_velocidad = e.find("h4")
            
            tag_div_fijo = e.find("div", class_ = ["col_3"])
            tag_ul_fijo = tag_div_fijo.find("ul")
            tag_fijo = tag_ul_fijo.find("li")
            fijo = tag_fijo.string
            tag_li_min_fijo = tag_ul_fijo.find_all("li")
            for i in tag_li_min_fijo:
                tag_min_fijo = i.string.strip()
            
            tag_div_movil = e.find("div", class_ = ["col_4"])
            tag_ul_movil = tag_div_movil.find("ul")
            tag_movil = tag_ul_movil.find("li")
            movil = tag_movil.string.strip()
            tag_li_gb_movil = tag_ul_movil.find_all("li")
            for i in tag_li_gb_movil:
                tag_gb_movil = i.string.strip()
                
            tag_div_tv = e.find("div", class_ = ["col_5"])
            tag_p_tv = tag_div_tv.find("p")
            if(tag_p_tv == None):
                tv = "Sin TV"
            else:
                tv = tag_p_tv.string
            
            
            tag_ul_promo = e.find("ul", class_ = ["promo"])
            tag_promo = tag_ul_promo.find("li")
            if(tag_promo == None):
                promo = "Sin promoción"
            else:
                promo = tag_promo.string
            
            tag_div_precio = e.find("strong")
            
            nombre_tarifa = tag_nombre_tarifa.string.strip()
            velocidad = tag_velocidad.string.strip()
            movil = movil   
            
            precio = tag_div_precio.string.strip()
            
            paquete = [nombre_tarifa, velocidad, fijo + '. ' + tag_min_fijo, movil + '. ' + tag_gb_movil, tv, promo, precio+' €']
            
            lista_paquetes.append(paquete)
        
    return (lista_paquetes)

def seleccionar_pagina():
    url = "https://www.phonehouse.es/tarifas/vodafone/one.html"
    paginas = []
    
    paginas.append(url)
    for i in range (2, 6):
        p = url + "?convergente-pagina=" + str(i) + "#convergente"
        paginas.append(p)
    
    return paginas

def procesar_pagina(d:str):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, "lxml")
    return documento

#print(cargar_paquetes())

