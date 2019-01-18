from principal.models import Tarifa_movil, ADSL_FIBRA, Paquete, Operadora

def deleteTables():
    Tarifa_movil.objects.all().delete()
    ADSL_FIBRA.objects.all().delete()
    Paquete.objects.all().delete()
    Operadora.objects.all().delete()
    

def populateFromVodafone():
    pass


def populateFromYoigo():
    pass


def populateFromOrange():
    pass


def populateDatabase():
    deleteTables()
    
    populateFromYoigo()
    populateFromOrange()
    populateFromVodafone()
    
    print("Finished database population...")
    

if __name__ == '__main__':
    populateDatabase()
    


