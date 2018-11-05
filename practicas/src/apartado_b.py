# encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3


def ordenar_precio():
    conn = sqlite3.connect('productos.db')
    conn.text_factory = str 
    cursor = conn.execute("SELECT DENOMINACION,PRECIO FROM PRODUCTOS ORDER BY PRECIO ASC")
    imprimir_aceites_denominacion_precio(cursor)
    conn.close
    
    
def imprimir_aceites_denominacion_precio(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, "Denominación: " +row[1])
        lb.insert(END, "Precio: " + row[2])
        lb.insert(END, "")
        
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)
        

def imprimir_aceites_denominacion(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, "Denominación: " +row[1])
        lb.insert(END, "")
        
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)
