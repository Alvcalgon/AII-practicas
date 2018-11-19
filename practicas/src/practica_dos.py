'''
Created on 18 nov. 2018

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
from whoosh.qparser import QueryParser, MultifieldParser

from bs4 import BeautifulSoup


dir_index = "Index_noticias"


def seleccionar_pagina2():
    url = "https://www.ecartelera.com/noticias/"
    paginas = []
    
    paginas.append(url)
    for i in range (2, 4):
        p = url + "lista/" + str(i) + "/"
        paginas.append(p)
    
    return paginas

# Que indica la pareja d:str???
def procesar_pagina(d:str):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, "lxml")
    return documento

def extraer_datos():
    lista_noticias = []
    
    paginas = seleccionar_pagina2()
    print("Paginas de temas", len(paginas))
    
    for pagina in paginas:
        print(pagina)
        documento = procesar_pagina(pagina)
        
        # l almacena las etiquetas que contiene
        # cada uno de las noticias publicados.
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
            print(fecha)
            
            f =formatear_fecha(fecha)
            
            noticia = [antetitulo, titulo, enlace_imagen, descripcion, f]
            lista_noticias.append(noticia)
            
    return lista_noticias


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
             "noviembre":"11",
             "Noviembr":"11",
             "noviembr":"11",
             "Diciembre":"12"}
    
    fecha = re.match(r'.*(\d\d)\s*.{2}\s*([a-zA-Z]{3,})\s*.{2}\s*(\d{4}).*', date)
    # Groups devuelve las cadenas (o subcadenas) que coinciden con el patron
    l = list(fecha.groups())
    l[1] = meses[l[1]]
    
    result = l[2] + l[1] + l[0]
    
    return result    

def cargar():
    noticias = extraer_datos()
    i = 0
    
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)
        
    ix = create_in(dir_index, schema = definir_esquema())
    
    writer = ix.writer()
    
    for noticia in noticias:
        add_doc(writer, noticia)
        i += 1
        
    writer.commit()
    
    messagebox.showinfo("Fin de indexado", "Se han indexado " + str(i) + " noticias.")
    

def add_doc(writer, noticia):
    writer.add_document(antetitulo = noticia[0],
                        titulo = noticia[1],
                        enlaceImagen = noticia[2],
                        descripcion = noticia[3],
                        fechaPublicacion = datetime.strptime(noticia[4], '%Y%m%d'))


def definir_esquema():
    return Schema(antetitulo=TEXT(stored = True),
                  titulo=TEXT(stored = True),
                  enlaceImagen=ID(stored = True),
                  descripcion=TEXT,
                  fechaPublicacion=DATETIME(stored = True))


def busqueda_titulo_descripcion():
    def mostrar_lista(event):
    
        lb.delete(0,END)
    
        ix = open_dir(dir_index)
        with ix.searcher() as searcher:
            query = MultifieldParser(["titulo","descripcion"], ix.schema).parse(str(en_tituloDescripcion.get()))
            results=searcher.search(query)
            for r in results:
                lb.insert(END, "Antetitulo: " + r['antetitulo'])
                lb.insert(END, "Titulo: " + r['titulo'])
                lb.insert(END, "Fecha publicacion: " + r['fechaPublicacion'].strftime('%Y/%m/%d'))
                lb.insert(END, "")

    v = Toplevel()
    v.title("Busqueda por titulo y descripcion")    
    
    f = Frame(v)
    f.pack(side = TOP)    
    
    label = Label(f, text = "Introduzca titulo y descripcion: ")
    label.pack(side = LEFT)
    
    en_tituloDescripcion = Entry(f)
    en_tituloDescripcion.bind("<Return>", mostrar_lista)
    en_tituloDescripcion.pack(side = LEFT)

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
            my_query = "{" + str(en_fecha_comienzo.get()) + " TO " + str(en_fecha_fin.get()) + "}"
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
    buscarmenu = Menu(menubar, tearoff = 0)
    buscarmenu.add_command(label = "Titulo y descripcion", command = busqueda_titulo_descripcion)
    buscarmenu.add_command(label = "Fecha", command = busqueda_fecha)
    buscarmenu.add_command(label = "Descripcion", command = busqueda_descripcion)
    menubar.add_cascade(label = "Buscar", menu = buscarmenu)
    
    
    root.config(menu = menubar)
    root.mainloop()

if __name__ == '__main__':
    aplicacion()
    
    
    
    
    