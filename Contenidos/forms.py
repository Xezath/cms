from django import forms
from ckeditor.widgets import CKEditorWidget
from Categoria.models import Categoria
from Plantilla.models import Plantilla
from .models import Contenidos

class ContenidosForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),  # Aquí defines el queryset con las opciones
        widget=forms.Select,               # Esto asegura que se renderice como un <select>
        empty_label="Seleccione una categoría",  # Etiqueta para el valor vacío
        label="Categoría"            # Cambia la etiqueta si lo necesitas
    )
    plantilla = forms.ModelChoiceField(
        queryset=Plantilla.objects.all(), 
        required=False,
        widget=forms.Select,               # Esto asegura que se renderice como un <select>
        empty_label="Seleccione una plantilla",  # Etiqueta para el valor vacío
        label="Plantilla"
        )
    class Meta:
        model = Contenidos
        fields = '__all__'  
class EditarContenidosForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),  # Aquí defines el queryset con las opciones
        widget=forms.Select,               # Esto asegura que se renderice como un <select>
        empty_label="Seleccione una categoría",  # Etiqueta para el valor vacío
        label="Categoría"            # Cambia la etiqueta si lo necesitas
    )
    plantilla = forms.ModelChoiceField(
        queryset=Plantilla.objects.all(), 
        required=False,
        widget=forms.Select,               # Esto asegura que se renderice como un <select>
        empty_label="Seleccione una plantilla",  # Etiqueta para el valor vacío
        label="Plantilla"
        )
    class Meta:
        model = Contenidos
        fields = '__all__'

class VisualizarContenidoForm(forms.ModelForm):
    plantilla = forms.ModelChoiceField(
        queryset=Plantilla.objects.all(), 
        required=False,
        widget=forms.Select,               # Esto asegura que se renderice como un <select>
        empty_label="Seleccione una plantilla",  # Etiqueta para el valor vacío
        label="Plantilla"
        )
    class Meta:
        model = Contenidos
        fields = '__all__'