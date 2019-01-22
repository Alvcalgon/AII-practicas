# -*- encoding: utf-8 -*-
from django import forms

class tarifaForm(forms.Form):
    search = forms.CharField(label='search ID')
    
