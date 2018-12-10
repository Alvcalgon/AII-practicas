from django.db import models

# Create your models here.
class Banco(models.Model):
    entidadId = models.CharField(max_length = 4, primary_key = True)
    nombre = models.CharField(max_length = 50)
    
    def __str__(self):
        return "ID: " + self.entidadId + " Nombre: " + self.nombre


class Sucursal(models.Model):
    sucursalId = models.CharField(max_length = 4, primary_key = True)
    direccion = models.CharField(max_length = 80)
    telefono = models.CharField(max_length = 9)
    banco = models.ForeignKey(Banco, on_delete = models.CASCADE)
    
    def __str__(self):
        return "ID: " + self.sucursalId
    
class Usuario(models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    email = models.EmailField()
    nombre = models.CharField(max_length = 50)
    apellidos = models.CharField(max_length = 80)
    bancos = models.ManyToManyField(Banco)
    
    def __str__(self):
        return "Nombre completo: " + self.nombre + " " + self.apellidos
    
class Cuenta(models.Model):
    numero = models.CharField(max_length = 20)
    usuarios = models.ManyToManyField(Usuario)
    saldo = models.FloatField()
    
    def __str__(self):
        return self.numero
    
    
class Movimiento(models.Model):
    fecha = models.DateField()
    numero = models.CharField(max_length = 20)
    descripcion = models.TextField()
    euros = models.FloatField()
    cuenta = models.ForeignKey(Cuenta, on_delete = models.CASCADE)
    
    def __str__(self):
        return "Fecha: " + self.fecha + " Montante: " + self.euros
    