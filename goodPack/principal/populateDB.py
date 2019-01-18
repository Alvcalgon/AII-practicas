from bs4 import BeautifulSoup

import urllib.request
import re

from principal.models import Tarifa_movil, ADSL_FIBRA, Paquete, Operadora


def deleteTables():
    Tarifa_movil.objects.all().delete()
    ADSL_FIBRA.objects.all().delete()
    Paquete.objects.all().delete()
    Operadora.objects.all().delete()


def populate_operator():
    w_nombre = "Vodafone"
    w_enlace = "https://www.vodafone.es/c/particulares/es/"
    w_telefono = "900921009"
    
    Operadora.objects.create(nombre = w_nombre, enlace_web = w_enlace, telefono = w_telefono)
    
    w_nombre = "Orange"
    w_enlace = "https://www.orange.es/"
    w_telefono = "900263159"
    
    Operadora.objects.create(nombre = w_nombre, enlace_web = w_enlace, telefono = w_telefono)
    
    w_nombre = "Yoigo"
    w_enlace = "https://www.yoigo.com/"
    w_telefono = "622"
    
    Operadora.objects.create(nombre = w_nombre, enlace_web = w_enlace, telefono = w_telefono)
    
    n = Operadora.objects.count()
    print(str(n) + " operators stored in DB.")
    
def populateFromVodafone():
    pass


def populateFromYoigo():
    print("Retrieving data from Yoigo...")
    
    pagina = "https://www.yoigo.com/tarifas-moviles"
    extraer_tarifas_moviles(pagina)
    
    """
    pagina = "https://www.yoigo.com/tarifas-tarjeta"
    extraer_tarifas_moviles(pagina)
    
    extraer_fibra_optica()
    
    extraer_paquete_fibra_y_movil()
    """
    print("Retrieved data from Yoigo...")
    
def populateFromOrange():
    pass


def populateDatabase():
    deleteTables()
    
    populate_operator()
    
    populateFromYoigo()
    #populateFromOrange()
    #populateFromVodafone()
    
    print("Finished database population...")
    

# Funciones y procedimientos relacionados con Beautifulsoup
def procesar_pagina(d):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, "lxml")
    return documento


def extraer_paquete_fibra_y_movil():
    pagina = "https://www.yoigo.com/fibra-optica"
    documento = procesar_pagina(pagina)
    lista_paquetes = documento.find_all("div", class_ = ["desktop", "desktop-wrapper"])
    
    n = len(lista_paquetes)
    
    for i in range(1,n):
        paquete = lista_paquetes[i]
        
        etiqueta_nombre = paquete.find("a", class_ = ["capitalized"])
        etiqueta_coste_pentera = paquete.find("span", class_ = ["price-offer"])
        etiqueta_coste_pdecimal = paquete.find("span", class_ = ["pricing-detail-fee", "truncate-text"])
        etiqueta_promociones = paquete.find("p", class_ = ["info",
                                                            "flex",
                                                            "flex-column",
                                                            "text-center",
                                                            "ng-star-inserted"])
        
        w_nombre = etiqueta_nombre.string.strip()
        
        w_velocidad = re.compile("(\d+\s*\w{2})").search(w_nombre).group(0)
        
        w_movil = w_nombre.split("+")
        
        if re.compile("\d+\s*\w*").search(w_movil[1].strip()):
            w_datos = re.compile("\d+\s*\w*").search(w_movil[1].strip()).group(0)
        else:
            w_datos = "GB infinitos"
        
        w_fijo = "Llamadas infinitas"
        w_tv = ""
        
        w_promociones = ""
        for hijo in etiqueta_promociones.contents:
            w_promociones = w_promociones + " " + hijo.string.strip() + " "
            
        w_promociones.strip()
        
        promo = w_promociones[1:]
        
        coste_entera = etiqueta_coste_pentera.string.strip()
        coste_decimal = re.compile('\d{2}').search(etiqueta_coste_pdecimal.string.strip()).group(0)
            
        w_coste_mensual = coste_entera + "." + coste_decimal
        
        yoigo = Operadora.objects.get(nombre = 'Yoigo')
           
        Paquete.objects.create(nombre = w_nombre,
                               velocidad = w_velocidad,
                               fijo = w_fijo,
                               movil = w_datos,
                               tv = w_tv,
                               promociones = promo,
                               coste_mensual = w_coste_mensual,
                               operadora = yoigo)
    
    n = Paquete.objects.count()
    print(str(n) + " paquetes almacenados.")

def extraer_fibra_optica():
    pagina = "https://www.yoigo.com/solo-internet"
    documento = procesar_pagina(pagina)
    lista_fibras = documento.find_all("div", class_ = ["desktop", "desktop-wrapper"])
    
    n = len(lista_fibras)
    
    for i in range(1,n):
        fibra = lista_fibras[i]
        
        etiqueta_nombre = fibra.find("a", class_ = ["capitalized"])        
        etiqueta_coste_pentera = fibra.find("span", class_ = ["price-offer"])
        etiqueta_coste_pdecimal = fibra.find("span", class_ = ["pricing-detail-fee", "truncate-text"])
        etiqueta_fijo = fibra.find_all("p", class_ = ["info",
                                                      "flex",
                                                      "flex-column",
                                                      "text-center"])
        etiqueta_hija_fijo = etiqueta_fijo[1]
        etiqueta_promociones = fibra.find("p", class_ = ["cloud-sticker__text",
                                                         "cloud-sticker__text--desktop",
                                                         "flex",
                                                         "flex-column",
                                                         "flex-center-center"])
        etiqueta_promo = etiqueta_coste_pdecimal.next_sibling
        etiqueta_promocion = etiqueta_promo.find("span", class_ = ["ng-star-inserted"])
        
        w_nombre = etiqueta_nombre.string.strip()
        
        coste_entera = etiqueta_coste_pentera.string.strip()
        coste_decimal = re.compile('\d{2}').search(etiqueta_coste_pdecimal.string.strip()).group(0)
            
        w_coste_mensual = coste_entera + "." + coste_decimal
        
        w_promociones = ""
        if etiqueta_promociones:
            for hijo in etiqueta_promociones:
                child = hijo.string.strip()
                w_promociones = w_promociones + child + " "
    
        
        periodo = etiqueta_promocion.contents[0]
        
        if not periodo.startswith('IVA'):
            w_promociones.strip()
            w_promociones = w_promociones + periodo
        
        w_promociones.strip()
        
        w_velocidad = re.compile("\d{1,}\s+\w*$").search(w_nombre).group(0)
        w_tipo = "Fibra"
        w_fijo = ""
        for hijo in etiqueta_hija_fijo:
            w_fijo = w_fijo + hijo.string.strip() + " "
        
        yoigo = Operadora.objects.get(w_nombre = 'Yoigo')
        
        ADSL_FIBRA.objects.create(nombre = w_nombre,
                                  velocidad = w_velocidad,
                                  fijo = w_fijo,
                                  promociones = w_promociones,
                                  coste_mensual = w_coste_mensual,
                                  tipo = w_tipo,
                                  operadora = yoigo)
    
    n = ADSL_FIBRA.objects.count()
    print(str(n) + " tarifas de fibra almacenadas")     

def extraer_tarifas_moviles(pagina):
    documento = procesar_pagina(pagina)
    lista_tarifas = documento.find_all("div", class_ = ["desktop", "desktop-wrapper"])
    
    n = len(lista_tarifas)
    
    for i in range(1,n):
        tarifa = lista_tarifas[i]
        
        etiqueta_nombre = tarifa.find("a", class_ = ["capitalized"])
        etiqueta_datosMin = tarifa.find_all("span", class_ = ["big"])
        
        w_nombre = etiqueta_nombre.string.strip()
        w_internet_movil = etiqueta_datosMin[0].string.strip()
        w_minutos = etiqueta_datosMin[1].string.strip()
        
        if pagina == "https://www.yoigo.com/tarifas-moviles":
            etiqueta_coste_mensual = tarifa.find("div", class_ = ["total-no-promotion",
                                                                  "ng-star-inserted"])
            etiqueta_coste = etiqueta_coste_mensual.contents[0]
            etiqueta_promociones = tarifa.find("p", class_ = ["cloud-sticker__text",
                                                              "cloud-sticker__text--desktop",
                                                              "flex",
                                                              "flex-column",
                                                              "flex-center-center"])
            w_promociones = ""
            for hijo in etiqueta_promociones:
                w_promociones = w_promociones + hijo.string.strip() + " "
        
            w_promociones.strip()
            w_coste_mensual = re.compile('\d{2},\d{2}').search(etiqueta_coste.strip()).group(0)
            w_tipo = "Contrato"
        else:        
            etiqueta_coste_pentera = tarifa.find("span", class_ = ["price-offer"])
            etiqueta_coste_pdecimal = tarifa.find("span", class_ = ["pricing-detail-fee", "truncate-text"])
            
            coste_entera = etiqueta_coste_pentera.string.strip()
            coste_decimal = re.compile('\d{2}').search(etiqueta_coste_pdecimal.string.strip()).group(0)
    
            w_promociones = ""        
            w_coste_mensual = coste_entera + "." + coste_decimal 
            w_tipo = "Tarjeta"
        
        yoigo = Operadora.objects.get(w_nombre = 'Yoigo')
                      
        Tarifa_movil.objects.create(nombre = w_nombre,
                                    minutos = w_minutos,
                                    internet_movil = w_internet_movil,
                                    promociones = w_promociones,
                                    coste_mensual = w_coste_mensual,
                                    tipo = w_tipo,
                                    operadora = yoigo)
    
    n = Tarifa_movil.objects.count()
    print(str(n) + " tarifas moviles almacenadas.")

if __name__ == '__main__':
    populateDatabase()
    


