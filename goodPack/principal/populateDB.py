#encoding: utf-8
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
    print("Extrayendo datos de Yoigo...")
    
    pagina = "https://www.yoigo.com/tarifas-moviles"
    extraer_tarifas_moviles_yoigo(pagina)
    
    
    pagina = "https://www.yoigo.com/tarifas-tarjeta"
    extraer_tarifas_moviles_yoigo(pagina)
    
    
    extraer_fibra_optica_yoigo()
    
    extraer_paquete_yoigo()
    
    print("Datos de Yoigo extraidos...")
    
def populateFromOrange():
    print("")
    
    #extraer_tarifas_moviles_orange()
    #extraer_adsl_fibra_orange()
    extraer_paquetes_orange()
    
    print("")


def populateDatabase():
    deleteTables()
    
    populate_operator()
    
    #populateFromYoigo()
    populateFromOrange()
    #populateFromVodafone()
    
    print("Finished database population...")
    

# Funciones y procedimientos relacionados con Beautifulsoup
def procesar_pagina(d):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, "lxml")
    return documento

def seleccionar_pagina():
    url = "https://www.phonehouse.es/tarifas/orange/love.html"
    paginas = []
    
    paginas.append(url)
    for i in range (2, 8):
        p = url + "?convergente-pagina=" + str(i) + "#convergente"
        paginas.append(p)
    
    return paginas


# Beautifulsoup sobre Yoigo

def extraer_paquete_yoigo():
    pagina = "https://www.yoigo.com/fibra-optica"
    documento = procesar_pagina(pagina)
    lista_paquetes = documento.find_all("div", class_ = ["desktop", "desktop-wrapper"])
    
    n = len(lista_paquetes)
    
    for i in range(1,n):
        paquete = lista_paquetes[i]
        
        w_nombre = getNombre(paquete)
        w_velocidad = getVelocidad(w_nombre, "(\d+\s*\w{2})")
        w_fijo = "Llamadas infinitas"
        w_tv = ""
        w_promociones = getPromociones(paquete, pagina)
        w_coste_mensual = getCosteMensual(paquete, pagina)
        yoigo = getOperadora('Yoigo')
        
        w_movil = w_nombre.split("+")
        
        if re.compile("\d+\s*\w*").search(w_movil[1].strip()):
            w_datos = re.compile("\d+\s*\w*").search(w_movil[1].strip()).group(0)
        else:
            w_datos = "GB infinitos"
        
           
        Paquete.objects.create(nombre = w_nombre,
                               velocidad = w_velocidad,
                               fijo = w_fijo,
                               movil = w_datos,
                               tv = w_tv,
                               promociones = w_promociones,
                               coste_mensual = w_coste_mensual,
                               operadora = yoigo)
    
    n = Paquete.objects.count()
    print(str(n) + " paquetes almacenados.")

def extraer_fibra_optica_yoigo():
    pagina = "https://www.yoigo.com/solo-internet"
    documento = procesar_pagina(pagina)
    lista_fibras = documento.find_all("div", class_ = ["desktop", "desktop-wrapper"])
    
    n = len(lista_fibras)
    
    for i in range(1,n):
        fibra = lista_fibras[i]
                
        etiqueta_fijo = fibra.find_all("p", class_ = ["info",
                                                      "flex",
                                                      "flex-column",
                                                      "text-center"])
        etiqueta_hija_fijo = etiqueta_fijo[1]
        
        etiqueta_coste_pdecimal = fibra.find("span", class_ = ["pricing-detail-fee", "truncate-text"])
        etiqueta_promo = etiqueta_coste_pdecimal.next_sibling
        etiqueta_promocion = etiqueta_promo.find("span", class_ = ["ng-star-inserted"])
        
        w_nombre = getNombre(fibra)
        w_coste_mensual = getCosteMensual(fibra, pagina)
        w_velocidad = getVelocidad(w_nombre, "\d{1,}\s+\w*$")
        w_tipo = "Fibra"
        yoigo = getOperadora('Yoigo')
        
        w_promociones = getPromociones(fibra, pagina)
    
        periodo = etiqueta_promocion.contents[0]
        
        if not periodo.startswith('IVA'):
            w_promociones.strip()
            w_promociones = w_promociones + periodo
        
        w_promociones.strip()
        
        w_fijo = ""
        for hijo in etiqueta_hija_fijo:
            w_fijo = w_fijo + hijo.string.strip() + " "
        
        ADSL_FIBRA.objects.create(nombre = w_nombre,
                                  velocidad = w_velocidad,
                                  fijo = w_fijo,
                                  promociones = w_promociones,
                                  coste_mensual = w_coste_mensual,
                                  tipo = w_tipo,
                                  operadora = yoigo)
    
    n = ADSL_FIBRA.objects.count()
    print(str(n) + " tarifas de fibra (o ADSL) almacenadas")     

def extraer_tarifas_moviles_yoigo(pagina):
    documento = procesar_pagina(pagina)
    lista_tarifas = documento.find_all("div", class_ = ["desktop", "desktop-wrapper"])
    
    n = len(lista_tarifas)
    
    for i in range(1,n):
        tarifa = lista_tarifas[i]
        
        etiqueta_datosMin = tarifa.find_all("span", class_ = ["big"])
        
        w_nombre = getNombre(tarifa)
        w_internet_movil = etiqueta_datosMin[0].string.strip()
        w_minutos = etiqueta_datosMin[1].string.strip()
        w_promociones = getPromociones(tarifa, pagina)
        w_coste_mensual = getCosteMensual(tarifa, pagina)
        w_tipo = "Contrato" if pagina == "https://www.yoigo.com/tarifas-moviles" else "Tarjeta"
        yoigo = getOperadora('Yoigo')
    
        Tarifa_movil.objects.create(nombre = w_nombre,
                                    minutos = w_minutos,
                                    internet_movil = w_internet_movil,
                                    promociones = w_promociones,
                                    coste_mensual = w_coste_mensual,
                                    tipo = w_tipo,
                                    operadora = yoigo)
    
    n = Tarifa_movil.objects.count()
    print(str(n) + " tarifas moviles almacenadas.")


def getNombre(elemento_tag):
    etiqueta_nombre = elemento_tag.find("a", class_ = ["capitalized"])
    result = etiqueta_nombre.string.strip()
    return result

def getVelocidad(nombre, patron):
    result = re.compile(patron).search(nombre).group(0)
    return result

def getOperadora(name):
    return Operadora.objects.get(nombre = name)

def getPromociones(elemento_tag, pagina):
    if pagina == "https://www.yoigo.com/fibra-optica":
        result = ""
        etiqueta_promociones = elemento_tag.find("p", class_ = ["info",
                                                           "flex",
                                                           "flex-column",
                                                           "text-center",
                                                           "ng-star-inserted"])
        
        for hijo in etiqueta_promociones.contents:
            child = hijo.string.strip()
            result = result + " " + child + " "
            
        result.strip()
        return result[1:]
    else:
        result = ""
        etiqueta_promociones = elemento_tag.find("p", class_ = ["cloud-sticker__text",
                                                                "cloud-sticker__text--desktop",
                                                                "flex",
                                                                "flex-column",
                                                                "flex-center-center"])
        if etiqueta_promociones:
            for hijo in etiqueta_promociones:
                child = hijo.string.strip()
                result = result + child + " "
                
            result.strip()
            
        return result

    
def getCosteMensual(elemento_tag, pagina):
    if pagina == "https://www.yoigo.com/tarifas-moviles":
        etiqueta_coste_mensual = elemento_tag.find("div", class_ = ["total-no-promotion",
                                                                    "ng-star-inserted"])
        etiqueta_coste = etiqueta_coste_mensual.contents[0]
        result = re.compile('\d{2},\d{2}').search(etiqueta_coste.strip()).group(0)
        result = result.replace(",", ".")
        return float(result)
    else:
        etiqueta_coste_pentera = elemento_tag.find("span", class_ = ["price-offer"])
        etiqueta_coste_pdecimal = elemento_tag.find("span", class_ = ["pricing-detail-fee",
                                                                      "truncate-text"])
        coste_entera = etiqueta_coste_pentera.string.strip()
        coste_decimal = re.compile('\d{2}').search(etiqueta_coste_pdecimal.string.strip()).group(0)
            
        result = coste_entera + "." + coste_decimal
        return float(result) 
    

# Beautifulsoup sobre Orange

def extraer_tarifas_moviles_orange():
    pagina = "https://www.phonehouse.es/tarifas/orange/movil-contrato.html"
    documento = procesar_pagina(pagina)
    
    l = documento.find_all("li", class_=["linea"])
    
    for e in l:
        tag_nombre_tarifa = e.find("div", class_ = ["nombre-tarifa"])

        tag_div_minutos_tarifa = e.find("div", class_ = ["col_2"])
        tag_minutos_tarifa = tag_div_minutos_tarifa.find("ul")
                
         
        tag_div_internet_tarifa = e.find("div", class_ = ["col_3"])
        tag_internet_tarifa = tag_div_internet_tarifa.find("li")
         
        tag_ul_promocion_tarifa = e.find("ul", class_= ["promo"])
        tag_promocion_tarifa = tag_ul_promocion_tarifa.find("li")
        
             
        tag_div_precio_tarifa = e.find("div", class_ = ["precio"])
        tag_precio_tarifa = tag_div_precio_tarifa.find("strong")
        precio_tarifa = tag_precio_tarifa.string.strip()
                          
        nombre_tarifa = tag_nombre_tarifa.string.strip()
        
        minutos_tarifa = tag_minutos_tarifa.string
        
        internet_tarifa = tag_internet_tarifa.string.strip()
        
        promocion_tarifa = tag_promocion_tarifa.string.strip()
        
        precio_tarifa = tag_precio_tarifa.string.strip()
        precio_tarifa = precio_tarifa.replace(",", ".")
         
        tipo_tarifa = "Contrato"
        
        orange = getOperadora('Orange')
    
        if (minutos_tarifa == None):
            minutos_tarifa = tag_minutos_tarifa.find(string = re.compile(""))
        elif (promocion_tarifa == None):
            promocion_tarifa = "Sin promocion"
        
        Tarifa_movil.objects.create(nombre = nombre_tarifa,
                                    minutos = minutos_tarifa,
                                    internet_movil = internet_tarifa,
                                    promociones = promocion_tarifa,
                                    coste_mensual = float(precio_tarifa),
                                    tipo = tipo_tarifa,
                                    operadora = orange)
    
    n = Tarifa_movil.objects.count()
    print(str(n) + " tarifas moviles almacenadas.")
    

def extraer_adsl_fibra_orange():
    pagina = "https://www.phonehouse.es/tarifas/orange/adsl-fibra.html"
    documento = procesar_pagina(pagina)
    
    l = documento.find_all("li", class_=["linea"])
    
    for e in l:
        tag_nombre_tarifa = e.find("div", class_ = ["nombre-tarifa"])
        tag_velocidad_adsl = e.find("h4")
        
        tag_div_fijo = e.find("div", class_ = ["col_3"])
        tag_ul_fijo = tag_div_fijo.find("ul")
        tag_fijo = tag_ul_fijo.find("li")
        fijo_tarifa = tag_fijo.string.strip()
        tag_nacionales = tag_ul_fijo.find_all("li")
        for i in tag_nacionales:
            tag_nacionales = i.string.strip()
        
        #for i in tag_fijo:
            #fijo_tarifa = i.string.strip()
        
        tag_ul_promo = e.find("ul", class_ = ["promo"])
        tag_promo = tag_ul_promo.find("li")
        tag_div_precio = e.find("strong")
        
        nombre_tarifa = tag_nombre_tarifa.string.strip()
        velocidad_adsl = tag_velocidad_adsl.string.strip()
        fijo_tarifa = fijo_tarifa + ' ' + tag_nacionales
        promo = tag_promo.string.strip()
        precio = tag_div_precio.string.strip()
        precio = precio.replace(",", ".")
        tipo_tarifa = re.compile("Fibra|ADSL").search(nombre_tarifa).group(0)
        orange = getOperadora('Orange')
        
        ADSL_FIBRA.objects.create(nombre = nombre_tarifa,
                                  velocidad = velocidad_adsl,
                                  fijo = fijo_tarifa,
                                  promociones = promo,
                                  coste_mensual = float(precio),
                                  tipo = tipo_tarifa,
                                  operadora = orange)
    
    n = ADSL_FIBRA.objects.count()
    print(str(n) + " tarifas de fibra (o ADSL) almacenadas")


def extraer_paquetes_orange():
    paginas = seleccionar_pagina()
    print("Paginas de paquetes Orange", len(paginas))
    for pagina in paginas:
        print(pagina)
        documento = procesar_pagina(pagina)
        l = documento.find_all("li", class_=["linea"])
        for e in l:
            tag_nombre_tarifa = e.find("div", class_ = ["nombre-tarifa"])
            tag_velocidad = e.find("h4")
            
            tag_div_fijo = e.find("div", class_ = ["col_3"])
            tag_ul_fijo = tag_div_fijo.find("ul")
            tag_fijo = tag_ul_fijo.find("li")
            fijo_tarifa = tag_fijo.string
            tag_li_min_fijo = tag_ul_fijo.find_all("li")
            for i in tag_li_min_fijo:
                tag_min_fijo = i.string.strip()
            
            tag_div_movil = e.find("div", class_ = ["col_4"])
            tag_ul_movil = tag_div_movil.find("ul")
            tag_movil = tag_ul_movil.find("li")
            movil_tarifa = tag_movil.string.strip()
            tag_li_gb_movil = tag_ul_movil.find_all("li")
            for i in tag_li_gb_movil:
                tag_gb_movil = i.string.strip()
                
            tag_div_tv = e.find("div", class_ = ["col_5"])
            tag_p_tv = tag_div_tv.find("p")
            if(tag_p_tv == None):
                tv_tarifa = "Sin TV"
            else:
                tv_tarifa = tag_p_tv.string
            
            
            tag_ul_promo = e.find("ul", class_ = ["promo"])
            tag_promo = tag_ul_promo.find("li")
            if(tag_promo == None):
                promo = "Sin promoción"
            else:
                promo = tag_promo.string
            
            tag_div_precio = e.find("strong")
            
            nombre_tarifa = tag_nombre_tarifa.string.strip()
            velocidad_tarifa = tag_velocidad.string.strip()
            movil_tarifa = movil_tarifa + '. ' + tag_gb_movil
            fijo_tarifa = fijo_tarifa + '. ' + tag_min_fijo
            precio = tag_div_precio.string.strip()
            precio = precio.replace(",", ".")
            orange = getOperadora('Orange')
            """
            print(nombre_tarifa + " - " + str(type(nombre_tarifa)) + " - " + str(len(nombre_tarifa)))
            print(velocidad_tarifa + " - " + str(type(velocidad_tarifa)))
            print(fijo_tarifa + " - " + str(type(fijo_tarifa)))
            print(movil_tarifa + " - " + str(type(movil_tarifa)))
            print(tv_tarifa + " - " + str(type(tv_tarifa)))
            print(precio + " - " + str(type(precio)))
            print("---")
            
            """
            Paquete.objects.create(nombre = nombre_tarifa,
                                   velocidad = velocidad_tarifa,
                                   fijo = fijo_tarifa,
                                   movil = movil_tarifa,
                                   tv = tv_tarifa,
                                   promociones = promo,
                                   coste_mensual = float(precio),
                                   operadora = orange)
    
    n = Paquete.objects.count()
    print(str(n) + " paquetes almacenados.")
        
if __name__ == '__main__':
    populateDatabase()
    


