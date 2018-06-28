from django import forms
from django.core import validators
import funcs.functions
    
class FormName(forms.Form):
    price = forms.FloatField(label="Precio")
    riskfree = forms.FloatField(label="Tasa libre de riesgo")
    symbol = forms.CharField(label="Símbolo", \
                             widget=forms.Select(choices= funcs.functions.get_symbols()))
    exercise_time = forms.IntegerField(label="Tiempo de ejercicio (Meses)")
    type_opt = forms.CharField(label='Tipo de Opcion', \
                                widget=forms.Select(choices=[("compra","Compra"), ("venta","Venta")]))
    botcatcher = forms.CharField(required=False, \
                                widget=forms.HiddenInput, \
                                validators=[validators.MaxLengthValidator(0)])
                                