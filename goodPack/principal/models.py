from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, URLValidator

# Create your models here.
class Operadora(models.Model):
    nombre = models.CharField(max_length = 30, blank = False)
    enlace_web = models.URLField(validators = [URLValidator()])
    telefono = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.nombre
    

class Tarifa_movil(models.Model):
    nombre = models.CharField(max_length = 50, blank = False)
    minutos = models.CharField(max_length = 50, blank = False)
    internet_movil = models.CharField(max_length = 30, blank = False)
    promociones = models.CharField(max_length = 75)
    coste_mensual = models.FloatField(validators = [MinValueValidator(0.0)])
    tipo = models.CharField(max_length = 20, validators = [RegexValidator('^Contrato|Tarjeta$',
                                                         'Una tarifa de movil es de Contrato o por Tarjeta ')])
    operadora = models.ForeignKey(Operadora, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.nombre
    

class ADSL_FIBRA(models.Model):
    nombre = models.CharField(max_length = 50, blank = False)
    velocidad = models.CharField(max_length = 30, blank = False)
    fijo = models.CharField(max_length = 40, blank = False)
    promociones = models.CharField(max_length = 75)
    coste_mensual = models.FloatField(validators = [MinValueValidator(0.0)])
    tipo = models.CharField(max_length = 20, validators = [RegexValidator('^Fibra|ADSL$',
                                                         'Fibra o ADSL. Ningun otro valor valido')])
    operadora = models.ForeignKey(Operadora, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
class Paquete(models.Model):
    nombre = models.CharField(max_length = 75, blank = False)
    velocidad = models.CharField(max_length = 30, blank = False)
    fijo = models.CharField(max_length = 60, blank = False)
    movil = models.CharField(max_length = 40, blank = False)
    tv = models.CharField(max_length = 50)
    promociones = models.CharField(max_length = 75)
    coste_mensual = models.FloatField(validators = [MinValueValidator(0.0)])
    operadora = models.ForeignKey(Operadora, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.nombre
         

    
