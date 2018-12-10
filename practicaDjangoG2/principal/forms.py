from django.forms import ModelForm
from principal.models import Banco, Sucursal, Usuario, Cuenta, Movimiento

class BancoForm(ModelForm):
    class Meta:
        model = Banco
        
class SucursalForm(ModelForm):
    class Meta:
        model = Sucursal
        
class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        
class CuentaForm(ModelForm):
    class Meta:
        model = Cuenta

class MovimientoForm(ModelForm):
    class Meta:
        model = Movimiento
        
        