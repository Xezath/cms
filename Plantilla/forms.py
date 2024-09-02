from django import forms
from .models import Plantilla

class CrearPlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = '__all__'

class EditarPlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = '__all__'

