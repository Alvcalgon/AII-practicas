'''
Created on 5 nov. 2018

@author: jesus
'''
# encoding:utf-8


def buscar_opiniones():
    def listar_aceites():
    
        conn = crear_conexion()# todos los aceites (nombre) que tengan opiniones de usuarios. 
        cursor=conn.execute("""SELECT * FROM PRODUCTOS WHERE OPINIONES > 0 """)
        imprimir_aceites_denominacion(cursor)
        cerrar_conexion(conn)
        
    
    

def imprimir_aceites_denominacion(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, "Denominacion: " +row[1])
        lb.insert(END, "")
        
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)
        

    