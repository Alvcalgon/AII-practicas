'''
Created on 19 nov. 2018

@author: Fernando
'''

# encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
from numba.cuda.api import stream
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME, NUMERIC, ID
from whoosh.qparser import QueryParser
from datetime import datetime
import sqlite3 as dbapi



def cargar():
    lista_noticias = []
    
    paginas = seleccionar_pagina2()
    print("Paginas de temas", len(paginas))
    for pagina in paginas:
        print(pagina)
        documento = procesar_pagina(pagina)
        # l almacena las etiquetas que contiene
        # cada uno de los temas publicados.
        l = documento.find_all("div", class_= ["story"])
        for e in l:
            tag_p_antetitulo = e.find("p", class_ = ["ant"])
            tag_scnt = e.find_all("div", class_= ["scnt"])
            for i in tag_scnt:
                tag_titulo = i.find("a")
                titulo = tag_titulo.string.strip()
            
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
                
                            
   
    
    
    

    
            

def seleccionar_pagina2():
    url = "https://www.ecartelera.com/noticias/"
    paginas = []
    
    paginas.append(url)
    for i in range (2, 5):
        p = url + "lista/" + str(i) + "/"
        paginas.append(p)
    
    return paginas

# Que indica la pareja d:str???
def procesar_pagina(d:str):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, "lxml")
    return documento


def formatear_fecha(date):
    meses = {"Enero":"01",
             "Febrero":"02",
             "Marzo":"03",
             "Abril":"04",
             "Mayo":"05",
             "Junio":"06",
             "Julio":"07",
             "Agosto":"08",
             "Septiembre":"09",
             "Octubre":"10",
             "Noviembre":"11",
             "Diciembre":"12"}
    fecha = re.match(r'.(\d\d)\s(.{3})\s*(\d{4}).*', date)
    # Groups devuelve las cadenas (o subcadenas) que coinciden con el patron
    l = list(fecha.groups())
    l[1] = meses[l[1]]
    return tuple(l)



def salir(root):
    root.destroy()


def aplicacion():
    root = Tk()
    root.geometry("200x100")
    
    menubar = Menu(root)
    
    # Opcion Datos
    datosmenu = Menu(menubar, tearoff = 0)
    datosmenu.add_command(label = "Cargar", command = cargar)
    datosmenu.add_command(label = "Salir", command = lambda: salir(root))
    menubar.add_cascade(label = "Datos", menu = datosmenu)
    
    # Opcion Buscar
#     buscarmenu = Menu(menubar, tearoff = 0)
#     buscarmenu.add_command(label = "Titulo y descripcion", command = busqueda_titulo_descripcion)
#     buscarmenu.add_command(label = "Fecha", command = busqueda_fecha)
#     buscarmenu.add_command(label = "Descripcion", command = busqueda_descripcion)
#     menubar.add_cascade(label = "Buscar", menu = buscarmenu)
    
    
    root.config(menu = menubar)
    root.mainloop()

if __name__ == '__main__':
    aplicacion()