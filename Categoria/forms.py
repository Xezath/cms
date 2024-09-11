from django import forms
from .models import Categoria
from .models import Subcategoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class SubcategoriaForm(forms.ModelForm):
    categoriaPadre = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),  # Aquí defines el queryset con las opciones
        widget=forms.Select,               # Esto asegura que se renderice como un <select>
        empty_label="Seleccione una categoría",  # Etiqueta para el valor vacío
        label="Categoría Padre"            # Cambia la etiqueta si lo necesitas
    )

    class Meta:
        model = Subcategoria
        fields = '__all__'

class EditarCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class EditarSubcategoriaForm(forms.ModelForm):
    categoriaPadre = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),  # Aquí defines el queryset con las opciones
        widget=forms.Select,               # Esto asegura que se renderice como un <select>
        empty_label="Seleccione una categoría",  # Etiqueta para el valor vacío
        label="Categoría Padre"            # Cambia la etiqueta si lo necesitas
    )
    class Meta:
        model = Subcategoria
        fields = '__all__'