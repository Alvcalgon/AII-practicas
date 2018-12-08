'''
Created on 19 nov. 2018

@author: Alvaro Calle Glez
'''

from tkinter import *
from tkinter import messagebox

import os
import re
from datetime import datetime

import urllib.request

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, DATETIME, NUMERIC
from whoosh.qparser import QueryParser

from bs4 import BeautifulSoup

dir_index = "Index_noticias"

def busqueda_descripcion():
    def mostrar_lista(event):
        lb.delete(0, END)
        
        ix = open_dir(dir_index)
        with ix.searcher() as searcher:
            query = QueryParser("descripcion", ix.schema).parse(str(en_descripcion.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END, "Antetitulo: " + r['antetitulo'])
                lb.insert(END, "Titulo: " + r['titulo'])
                lb.insert(END, "Enlace imagen: " + str(r['enlaceImagen']))
                lb.insert(END, "")
    
    v = Toplevel()
    v.title("Busqueda por descripcion")
    
    f = Frame(v)
    f.pack(side = TOP)
    
    label = Label(f, text = "Introduzca frase: ")
    label.pack(side = LEFT)
    
    en_descripcion = Entry(f)
    en_descripcion.bind("<Return>", mostrar_lista)
    en_descripcion.pack(side = LEFT)
    
    sc = Scrollbar(v)
    sc.pack(side = RIGHT, fill = Y)
    
    lb = Listbox(v, yscrollcommand = sc.set)
    lb.pack(side = BOTTOM, fill = BOTH)
    
    sc.config(command = lb.yview)
    
    
def busqueda_fecha():
    def mostrar_lista(event):
        lb.delete(0, END)
        
        ix = open_dir(dir_index)
        with ix.searcher() as searcher:
            my_query = str(en_fecha_comienzo.get()) + " TO " + str(en_fecha_fin)
            qp = QueryParser("fechaPublicacion", ix.schema)
            q = qp.parse(my_query)
            
            results = searcher.search(q)
            for r in results:
                lb.insert(END, "Titulo: " + r['titulo'])
                lb.insert(END, "Fecha publicacion: " + r['fechaPublicacion'].strftime('%Y/%m/%d'))
                lb.insert(END, "")
    
    v = Toplevel()
    v.title("Busqueda por rango de fecha")
    
    f = Frame(v)
    f.pack(side = TOP)
    
    label = Label(f, text = "Fecha comienzo: ")
    label.pack(side = LEFT)
    
    en_fecha_comienzo = Entry(f)
    en_fecha_comienzo.bind("<Return>", mostrar_lista)
    en_fecha_comienzo.pack(side = LEFT)
    
    label = Label(f, text = "Fecha fin: ")
    label.pack(side = LEFT)
    
    en_fecha_fin = Entry(f)
    en_fecha_fin.bind("<Return>", mostrar_lista)
    en_fecha_fin.pack(side = LEFT)
    
    
    sc = Scrollbar(v)
    sc.pack(side = RIGHT, fill = Y)
    
    lb = Listbox(v, yscrollcommand = sc.set)
    lb.pack(side = BOTTOM, fill = BOTH)
    
    sc.config(command = lb.yview)

if __name__ == '__main__':
    print("Hola")



