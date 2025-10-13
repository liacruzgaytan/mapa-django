from django import forms
from django.forms import inlineformset_factory
from .models import Pregunta, Opcion

class FormularioPregunta(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto_pregunta']

FormularioOpciones = inlineformset_factory(
    Pregunta, Opcion,
    fields=['texto_opcion'],
    extra=3,  # cuántas opciones mostrar por defecto
    can_delete=False
)
