from django.forms import ModelForm, forms
from principal.models import Banco, Sucursal, Usuario, Cuenta, Movimiento

class BancoForm(ModelForm):
    class Meta:
        model = Banco
        fields = ['entidadId','nombre']
        
class SucursalForm(ModelForm):
    class Meta:
        model = Sucursal
        fields = ['sucursalId','direccion','telefono','banco']
        
class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['username','password','email','nombre','apellidos','bancos']
        
class CuentaForm(ModelForm):
    class Meta:
        model = Cuenta
        fields = ['numero','usuarios','saldo']

class MovimientoForm(ModelForm):
    class Meta:
        model = Movimiento
        fields = ['fecha','numero','descripcion','euros','cuenta']
        
        
        