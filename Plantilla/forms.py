from django import forms
from .models import Plantilla

class CrearPlantillaForm(forms.ModelForm):
    """
    Formulario para crear una nueva Plantilla.

    Este formulario utiliza el modelo Plantilla y permite a los usuarios 
    ingresar todos los campos necesarios para crear una plantilla.
    """
    class Meta:
        model = Plantilla
        fields = '__all__'


class EditarPlantillaForm(forms.ModelForm):
    """
    Formulario para editar una Plantilla existente.

    Este formulario utiliza el modelo Plantilla y permite a los usuarios 
    modificar los campos de una plantilla ya creada.
    """
    class Meta:
        model = Plantilla
        fields = '__all__'