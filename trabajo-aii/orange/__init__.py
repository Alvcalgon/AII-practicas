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
    l = s.find_all("li", class_=["resultados"])
    return l

def cargar_tarifas_hablar_navegar():
    lista_tarifas = []
    
    l = extraer_tarifas_hablar_navegar()
    
    for e in l:
        tag_nombre_tarifa = e.find("div", class_ = ["nombre-tarifa"])
        tag_titulo_tabla = e.find_all("div", class_ = ["datos"])
        for i in tag_titulo_tabla:
            tag_titulo = i.find("div", class_ = ["titulo"])
            titulo = tag_titulo.string.strip()
            
            
        nombre_tarifa = tag_nombre_tarifa.string.strip()
        
        
        tag_enlace_imagen = e.find("img")
        tag_descripcion = e.find("p", class_=["desc"])
        tag_fecha = e.find("p", class_=["fec"])
        
        antetitulo = tag_p_antetitulo.string.strip()
        enlace_imagen = tag_enlace_imagen['src']
        descripcion = tag_descripcion.string.strip()
        fecha = tag_fecha.string.strip()
        
        
        noticia = [antetitulo, titulo, enlace_imagen, descripcion, fecha]
        lista_noticias.append(noticia)
        
        
        return (lista_noticias)
                
    