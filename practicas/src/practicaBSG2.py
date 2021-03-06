'''
Created on 5 nov. 2018

@author: Alvaro Calle Glez
'''
<<<<<<< HEAD
# encoding:utf-8
=======

>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
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
        
        tag_ul = documento.find("ul", class_ = ["products-grid", "isotope"])
        productos = tag_ul.find_all("li", class_ = ["item", "isotope-item"])
        
        for producto in productos:
            tag_producto = producto.find("div", class_ = ["product-shop"])
<<<<<<< HEAD
=======
            tag_pack = producto.find("div", class_ = ["amlabel-div", "test2"])
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
            
            tag_h2 = tag_producto.find("h2", class_ = ["product-name"])
            tag_box_price = tag_producto.find("div", class_ = ["price-box"])
            
            tag_deno = tag_h2.find("a")
            tag_enlace = producto.find("a")
            tag_reg_precio = tag_box_price.find("span", class_ = ["regular-price"])
<<<<<<< HEAD
            
=======
            tag_rating = tag_producto.find("div", class_ = ["ratings"])
            
            denominacion = tag_deno.string.strip()
            enlace = tag_enlace['href']
            
            formato = ""
            precio = "144,99"
            opiniones = 0
            
            if tag_pack != None:
                tag_formato = tag_pack.find("span", class_ = ["amlabel-txt"])
                if tag_formato != None and len(tag_formato.contents) == 3:
                    formato = tag_formato.contents[2]
                    
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
            if tag_reg_precio != None:
                tag_precio = tag_reg_precio.find("span", class_ = ["price"])
                if tag_precio != None:
                    precio = re.compile("^\d+(,\d+)?").search(tag_precio.string.strip()).group(0)
<<<<<<< HEAD
            else:
                precio = 144.99
            
            tag_rating = tag_producto.find("div", class_ = ["ratings"])
=======
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
            
            if tag_rating != None:
                tag_span = tag_rating.find("span", class_ = ["amount"])
                tag_a = tag_span.find("a")
                opiniones = int(re.compile("^\d+(,\d+)?").search(tag_a.string.strip()).group(0))
            
<<<<<<< HEAD
            else:
                opiniones = 0
            
            denominacion = tag_deno.string.strip()
            enlace = tag_enlace['href']
            precio = re.compile("^\d+(,\d+)?").search(tag_precio.string.strip()).group(0)
            formato = "Form"
            
=======
                        
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
            conn.execute("""INSERT INTO PRODUCTOS (DENOMINACION, ENLACE, PRECIO, OPINIONES, FORMATO_PACK)
                 VALUES (?, ?, ?, ?, ?)""", (denominacion,
                                                enlace,
                                                formatear_numero(precio),
<<<<<<< HEAD
                                                formato,
                                                opiniones))
            
        conn.commit()
        
        cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
        messagebox.showinfo("Base de datos", "Base de datos creada correctamente.\nHay " +
                         str(cursor.fetchone()[0]) + " registros.")
    
    cerrar_conexion(conn)

=======
                                                opiniones,
                                                formato))
            
    conn.commit()
        
    cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
    messagebox.showinfo("Base de datos", "Base de datos creada correctamente.\nHay " +
                     str(cursor.fetchone()[0]) + " registros.")
    
    cerrar_conexion(conn)


>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
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


def ordenar_precio():
<<<<<<< HEAD
    conn = crear_conexion() 
    cursor = conn.execute("SELECT DENOMINACION,PRECIO FROM PRODUCTOS ORDER BY PRECIO ASC")
    imprimir_aceites_denominacion_precio(cursor)
    cerrar_conexion(conn)
    

def buscar_opiniones():
    def listar_aceites():
    
        conn = crear_conexion()# todos los aceites (nombre) que tengan opiniones de usuarios. 
        cursor=conn.execute("""SELECT * FROM PRODUCTOS WHERE OPINIONES > 0 """)
        imprimir_aceites_denominacion(cursor)
        cerrar_conexion(conn)
=======
    conn = crear_conexion()
     
    cursor = conn.execute("SELECT DENOMINACION,PRECIO FROM PRODUCTOS ORDER BY PRECIO")
    imprimir_aceites_denominacion_precio(cursor)
    
    cerrar_conexion(conn)


def imprimir_aceites_denominacion_precio(cursor):
    v = Toplevel()
    
    sc = Scrollbar(v)
    sc.pack(side = RIGHT, fill = Y)
    
    lb = Listbox(v, width=150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, "Denominacion: " + row[0])
        lb.insert(END, "Precio: " + str(row[1]))
        lb.insert(END, "")
        
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)    

def buscar_opiniones():
    
    conn = crear_conexion() 
        
    cursor=conn.execute("SELECT DENOMINACION FROM PRODUCTOS WHERE OPINIONES > 0")
    imprimir_aceites_denominacion(cursor)
    
    cerrar_conexion(conn)
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
        
def mostrar_packs():
    def filtrar_busqueda(event):
        conn = crear_conexion()
        
        s_pack = "%" + en_pack.get() + "%"
        
<<<<<<< HEAD
        cursor = conn.execute("SELECT * FROM PRODUCTOS WHERE FORMATO_PACK LIKE ?",(s_pack))
        
=======
        cursor = conn.execute("SELECT DENOMINACION,PRECIO FROM PRODUCTOS WHERE FORMATO_PACK LIKE ?", (s_pack,))
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
        imprimir_aceites_denominacion_precio(cursor)
        
        cerrar_conexion(conn)
        
    v = Toplevel()
    
<<<<<<< HEAD
    label = Label(v, text="Seleccionar pack: ")
    label.pack(side=LEFT)
=======
    label = Label(v, text = "Seleccionar pack: ")
    label.pack(side = LEFT)
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
    
    packs = packs_db()
    
    en_pack = Spinbox(v, values = packs)
    en_pack.bind("<Return>", filtrar_busqueda)
<<<<<<< HEAD
    en_pack.pack(side=LEFT)
=======
    en_pack.pack(side = LEFT)
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
    
    
def packs_db():
    conn = crear_conexion()
    
<<<<<<< HEAD
    cursor = conn.execute("SELECT FORMATO_PACK FROM PRODUCTOS")
=======
    cursor = conn.execute("SELECT DISTINCT FORMATO_PACK FROM PRODUCTOS ORDER BY FORMATO_PACK")
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
    
    packs = [row[0] for row in cursor]
    
    cerrar_conexion(conn)
    
    return packs
    
<<<<<<< HEAD
    
def imprimir_aceites_denominacion_precio(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, "Denominacion: " +row[1])
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
        lb.insert(END, "Denominacion: " +row[1])
=======
            
def imprimir_aceites_denominacion(cursor):
    v = Toplevel()
    
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    
    lb = Listbox(v, width=150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, "Denominacion: " +row[0])
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
        lb.insert(END, "")
        
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)


def ventana_principal():
    top = Tk()
<<<<<<< HEAD
    almacenar = Button(top, text="Almacenar Aceites", command = cargar)
    almacenar.pack(side = TOP)
    Ordenar = Button(top, text="Ordenar por Precio", command = ordenar_precio)
    Ordenar.pack(side = TOP)
    Mostrar = Button(top, text="Mostrar Packs", command = mostrar_packs)
    Mostrar.pack(side = TOP)
    Buscar = Button(top, text="Buscar Opiniones", command = buscar_opiniones)
    Buscar.pack(side = TOP)
=======
    
    almacenar = Button(top, text="Almacenar Aceites", command = cargar)
    almacenar.pack(side = LEFT)
    
    Ordenar = Button(top, text="Ordenar por Precio", command = ordenar_precio)
    Ordenar.pack(side = LEFT)
    
    Mostrar = Button(top, text="Mostrar Packs", command = mostrar_packs)
    Mostrar.pack(side = LEFT)
    
    Buscar = Button(top, text="Buscar Opiniones", command = buscar_opiniones)
    Buscar.pack(side = LEFT)
    
>>>>>>> 5297b9636fccc907001d97af6bb5448e6e66e799
    top.mainloop()

if __name__ == '__main__':
    ventana_principal()