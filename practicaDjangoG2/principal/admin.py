from django.contrib import admin
from principal.models import Banco, Sucursal, Usuario, Cuenta, Movimiento

# Register your models here.
admin.site.register(Banco)
admin.site.register(Sucursal)
admin.site.register(Usuario)
admin.site.register(Cuenta)
admin.site.register(Movimiento)