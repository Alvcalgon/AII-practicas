
    
def ventana_principal():
    top = Tk()
    almacenar = Button(top, text="Almacenar Aceites", command = almacenar_bd)
    almacenar.pack(side = TOP)
    Ordenar = Button(top, text="Ordenar por Precio", command = ordenar_precio)
    Ordenar.pack(side = TOP)
    Mostrar = Button(top, text="Mostrar Packs", command = mostrar_packs)
    Mostrar.pack(side = TOP)
    Buscar = Button(top, text="Buscar Opiniones", command = buscar_opiniones)
    Buscar.pack(side = TOP)
    top.mainloop()
    

if __name__ == "__main__":
    ventana_principal()
