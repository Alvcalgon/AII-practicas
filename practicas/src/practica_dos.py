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
from whoosh.qparser import QueryParser

from bs4 import BeautifulSoup


def cargar():
    pass


def busqueda_titulo_descripcion():
    pass


def busqueda_fecha():
    pass


def busqueda_descripcion():
    pass


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