# encoding:utf-8
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.qparser import MultifieldParser
from tkinter import *
from tkinter import messagebox
from principal import populateDB
import sqlite3 as dbapi
import sqlite3

dir_in = "Index_goodPack"

def crear_conexion():
    conn = dbapi.connect("db.sqlite3")
    conn.text_factory = str
    return conn


def cerrar_conexion(conn):
    conn.close()
    
def definir_esquema_operadoras():
    return Schema(nombre=TEXT(stored=True),
                    enlace_web = ID(stored=True),
                    telefono = TEXT(stored=True))
    
def add_doc_operadora(writer, operadora):
    writer.add_document(nombre = operadora[0],
                        enlace_web = operadora[1],
                        telefono = operadora[2])
                    
def definir_esquema_tarifasMovil():
    return Schema(nombre=TEXT(stored=True),
                    minutos = TEXT(stored=True),
                    internet_movil = TEXT(stored=True),
                    promociones = TEXT(stored=True),
                    coste_mensual = NUMERIC(stored=True),
                    tipo = TEXT(stored=True),
                    operadora = TEXT(stored=True))
    
def add_doc_tarifaMovil(writer, tarifaMovil):
    writer.add_document(nombre = tarifaMovil[0],
                        minutos = tarifaMovil[1],
                        internet_movil = tarifaMovil[2],
                        promociones = tarifaMovil[3],
                        coste_mensual= float(tarifaMovil[4]),
                        tipo=tarifaMovil[5],
                        operadora=tarifaMovil[6])
                    
def definir_esquema_adslFibra():
    return Schema(nombre=TEXT(stored=True),
                    velocidad = TEXT(stored=True),
                    fijo = TEXT(stored=True),
                    promociones = TEXT(stored=True),
                    coste_mensual = NUMERIC(stored=True),
                    tipo = TEXT(stored=True),
                    operadora = TEXT(stored=True))
    
def add_doc_adslFibra(writer, adslFibra):
    writer.add_document(nombre = adslFibra[0],
                        velocidad = adslFibra[1],
                        fijo = adslFibra[2],
                        promociones = adslFibra[3],
                        coste_mensual= float(adslFibra[4]),
                        tipo=adslFibra[5],
                        operadora=adslFibra[6])
    
def definir_esquema_paquetes():
    return Schema(nombre=TEXT(stored=True),
                    velocidad = TEXT(stored=True),
                    fijo = TEXT(stored=True),
                    movil = TEXT(stored=True),
                    tv = TEXT(stored=True),
                    promociones = TEXT(stored=True),
                    coste_mensual = NUMERIC(stored=True),
                    operadora = TEXT(stored=True))
    
def add_doc_paquete(writer, paquete):
    writer.add_document(nombre = paquete[0],
                        velocidad = paquete[1],
                        fijo = paquete[2],
                        movil = paquete[3],
                        tv = paquete[4],
                        promociones = paquete[5],
                        coste_mensual= float(paquete[6]),
                        operadora=paquete[7])
    
    
def obtener_operadoras():
    conn = crear_conexion()
    
    cursor = conn.execute("SELECT NOMBRE,ENLACE_WEB,TELEFONO FROM OPERADORA")
    operadoras = [row for row in cursor]
    
    cerrar_conexion(conn)
    
    return operadoras

def obtener_tarifasMovil():
    conn = crear_conexion()
    
    cursor = conn.execute("SELECT NOMBRE,MINUTOS,INTERNET_MOVIL,PROMOCIONES,COSTE_MENSUAL,TIPO,OPERADORA FROM TARIFA_MOVIL")
    tarifaMovil = [row for row in cursor]
    
    cerrar_conexion(conn)
    
    return tarifaMovil

def obtener_adslFibra():
    conn = crear_conexion()
    
    cursor = conn.execute("SELECT NOMBRE,VELOCIDAD,FIJO,PROMOCIONES,COSTE_MENSUAL,TIPO,OPERADORA FROM ADSL_FIBRA")
    adslFibra = [row for row in cursor]
    
    cerrar_conexion(conn)
    
    return adslFibra

def obtener_paquetes():
    conn = crear_conexion()
    
    cursor = conn.execute("SELECT NOMBRE,VELOCIDAD,FIJO,MOVIL,TV,PROMOCIONES,COSTE_MENSUAL,OPERADORA FROM PAQUETE")
    paquete = [row for row in cursor]
    
    cerrar_conexion(conn)
    
    return paquete
                  
    
def indexar():
    if not os.path.exists(dir_in):
        os.mkdir(dir_in)
    
    ix_operadoras = create_in(dir_in,
                         schema = definir_esquema_operadoras(),
                         indexname = "indice_operadoras")
    
    ix_tarifasMovil = create_in(dir_in,
                                 schema= definir_esquema_tarifasMovil(),
                                 indexname = "indice_tarifasMovil")
    
    ix_adslFibra = create_in(dir_in,
                                 schema= definir_esquema_adslFibra(),
                                 indexname = "indice_adslFibra")
    
    ix_paquete = create_in(dir_in,
                                 schema= definir_esquema_paquetes(),
                                 indexname = "indice_paquetes")
    
    writer_operadoras = ix_operadoras.writer()
    i = 0
    for operadora in obtener_operadoras():
        add_doc_operadora(writer_operadoras, operadora)
        i += 1
    
    writer_tarifasMovil = ix_tarifasMovil.writer()    
    j = 0
    for tarifaMovil in obtener_tarifasMovil():
        add_doc_tarifaMovil(writer_tarifasMovil, tarifaMovil)
        j += 1
        
    writer_adslFibra = ix_adslFibra.writer()      
    k = 0
    for adslFibra in obtener_adslFibra():
        add_doc_adslFibra(writer_adslFibra, adslFibra)
        k += 1
        
    writer_paquetes = ix_paquete.writer()          
    l = 0
    for paquete in obtener_paquetes():
        add_doc_paquete(writer_paquetes, paquete)
        l += 1
        
    
    writer_operadoras.commit()
    writer_tarifasMovil.commit()
    writer_adslFibra.commit()
    writer_paquetes.commit()
    
    messagebox.showinfo("Fin de indexado", "Se han indexado " + str(i) + " operadoras.")
    messagebox.showinfo("Fin de indexado", "Se han indexado " + str(j) + " tarifas de movil.")
    messagebox.showinfo("Fin de indexado", "Se han indexado " + str(k) + " adsl y fibras.")
    messagebox.showinfo("Fin de indexado", "Se han indexado " + str(l) + " paquetes.")
    
    
# Búsquedas de tarifas movil   
def buscar_tarifas_movil():
    query = input("Introduzca una palabra de busqueda: ")
    ix = open_dir(dir_in, indexname= "indice_tarifasMovil")
    
    with ix.searcher() as searcher:
        myquery =  MultifieldParser(["internet_movil","coste_mensual"], ix.schema).parse(query)
        results = searcher.search(myquery)
        for r in results:
            print("Nombre: " + r['nombre'])
            print("Minutos: " + r['minutos'])
            print("Internet Movil: " + r['internet_movil'])
            print("Promociones: " + r['promociones'])
            print("Coste Mensual: " + r['coste_mensual'])
            print("Tipo: " + r['tipo'])
            print("Operadora: " + r['operadora'])
            print("")
            
# Busqueda de paquete
def buscar_paquete():
    query = input("Introduzca una palabra de busqueda: ")
    ix = open_dir(dir_in, indexname= "indice_paquetes")
    
    with ix.searcher() as searcher:
        myquery =  MultifieldParser(["velocidad","coste_mensual","nombre","tv"], ix.schema).parse(query)
        results = searcher.search(myquery)
        for r in results:
            print("Nombre: " + r['nombre'])
            print("Velocidad: " + r['velocidad'])
            print("Fijo: " + r['fijo'])
            print("Movil: " + r['movil'])
            print("TV: " + r['tv'])
            print("Promociones: " + r['promociones'])
            print("Coste Mensual: " + r['coste_mensual'])
            print("Operadora: " + r['operadora'])
            print("")
            
# Busqueda de adsl o fibra
def buscar_adsl_fibra():
    query = input("Introduzca una palabra de busqueda: ")
    ix = open_dir(dir_in, indexname= "indice_adslFibra")
    
    with ix.searcher() as searcher:
        myquery =  MultifieldParser(["velocidad","coste_mensual"], ix.schema).parse(query)
        results = searcher.search(myquery)
        for r in results:
            print("Nombre: " + r['nombre'])
            print("Velocidad: " + r['velocidad'])
            print("Fijo: " + r['fijo'])
            print("Promociones: " + r['promociones'])
            print("Coste Mensual: " + r['coste_mensual'])
            print("Tipo: " + r['tipo'])
            print("Operadora: " + r['operadora'])
            print("")

                
        
        
        
    
    
    

def ventana_principal():
    root = Tk()
    root.geometry("200x100")
    
    menubar = Menu(root)
    
    # Opcion Inicio    
    iniciomenu = Menu(menubar, tearoff = 0)
    iniciomenu.add_command(label = "Cargar", command = populateDB.populateDatabase())
    iniciomenu.add_command(label = "Indexar", command = indexar)
    iniciomenu.add_command(label = "Salir", command = root.destroy())
    menubar.add_cascade(label = "Inicio", menu = iniciomenu)
    
    # Opcion Buscar
    buscarmenu = Menu(menubar, tearoff = 0)
    
    tarifa_movil = Menu(buscarmenu, tearoff = 0)
    
    tarifa_movil.add_command(label = "Texto", command = buscar_tarifas_movil)
    buscarmenu.add_cascade(label = "Tarifas Movil", menu = tarifa_movil)
    
    paquete = Menu(buscarmenu, tearoff = 0)
    paquete.add_command(label = "Texto", command = buscar_paquete)
    buscarmenu.add_cascade(label = "Paquetes", menu = paquete)
    
    adsl_fibra = Menu(buscarmenu, tearoff = 0)
    adsl_fibra.add_command(label = "Texto", command = buscar_adsl_fibra)
    buscarmenu.add_cascade(label = "ADSL o Fibra", menu = adsl_fibra)
    
    menubar.add_cascade(label = "Buscar", menu = buscarmenu)
    
    root.config(menu = menubar)
    root.mainloop()
    

if __name__ == '__main__':
    ventana_principal()
    