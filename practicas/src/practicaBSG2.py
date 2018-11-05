'''
Created on 5 nov. 2018

@author: Alvaro Calle Glez
'''

import urllib.request

import sqlite3 as dbapi
from bs4 import BeautifulSoup

from tkinter import *
from tkinter import messagebox

import re


def crear_conexion():
    conn = dbapi.connect('productos.db')
    conn.text_factory = str
    return conn


def cerrar_conexion(conn):
    conn.close()


def cargar():
    conn = crear_conexion()
    
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS")
    conn.execute("""CREATE TABLE PRODUCTOS
        (DENOMINACION TEXT,
         ENLACE TEXT,
         PRECIO REAL,
         OPINIONES INTEGER,
         FORMATO_PACK TEXT);""")
    
    paginas = definir_pagina2()
    
    for pagina in paginas:
        print(pagina)
        documento = procesar_pagina(pagina)
        
        productos = documento.find_all("li", class_ = ["item"])
        
        for producto in productos:
            tag_producto = producto.find("div", class_ = ["product-shop"])
            tag_h2 = tag_producto.find("h2")
            tag_box_price = tag_producto.find("div", class_ = ["price-box"])
            
            tag_deno = tag_h2.find("a")
            tag_enlace = producto.find("a")
            tag_precio = tag_box_price.find_all("span", class_ = ["price"])
            
            tag_rating = tag_producto.find("div", class_ = ["ratings"])
            
            if tag_rating != None:
                tag_span = tag_rating.find("span", class_ = ["amount"])
                tag_a = tag_span.find("a")
                opiniones = int(re.compile("^\d+(,\d+)?").search(tag_a.string.strip()).group(0))
            
            else:
                opiniones = 0
            
            denominacion = tag_deno.string.strip()
            enlace = tag_enlace['href']
            precio = re.compile("^\d+(,\d+)?").search(tag_precio[1].string.strip()).group(0)
            formato = "Form"
            
            conn.execute("""INSERT INTO PRODUCTOS (DENOMINACION, ENLACE, PRECIO, OPINIONES, FORMATO_PACK)
                 VALUES (?, ?, ?, ?, ?, ?)""", (denominacion,
                                                enlace,
                                                formatear_numero(precio),
                                                formato,
                                                opiniones))
            
        conn.commit()
        
        cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
        messagebox.showinfo("Base de datos", "Base de datos creada correctamente.\nHay " +
                         str(cursor.fetchone()[0]) + " registros.")
    
    cerrar_conexion(conn)


def formatear_numero(precio):
    cadena_precio = ""
    
    for c in precio:
        if c != ",":
            cadena_precio += c
        else:
            cadena_precio += "."
    
    return float(cadena_precio)


def definir_pagina2():
    paginas = []
    
    url_uno = "https://www.origenoliva.com/aceite-de-oliva/mas-vendidos.html"
    url_dos = "https://www.origenoliva.com/aceite-de-oliva/mas-vendidos.html?p=2"
    
    paginas.append(url_uno)
    paginas.append(url_dos)
    
    return paginas


def procesar_pagina(d:str):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, 'lxml')
    
    return documento


def ventana_principal():
    top = Tk()
    
    almacenar = Button(top, text = "Almacenar", command = cargar)
    almacenar.pack(side = LEFT)
    
    
    top.mainloop()

if __name__ == '__main__':
    ventana_principal()