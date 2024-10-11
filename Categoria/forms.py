from django import forms
from .models import Categoria
from .models import Subcategoria

class CategoriaForm(forms.ModelForm):
    """
    Formulario para la creación de categorías.
    """
    class Meta:
        model = Categoria
        fields = '__all__'

class SubcategoriaForm(forms.ModelForm):
    """
    Formulario para la creación de subcategorías.
    Incluye un campo para seleccionar la categoría padre.
    """
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
    """
    Formulario para la edición de una categoría existente.
    """
    class Meta:
        model = Categoria
        fields = '__all__'

class EditarSubcategoriaForm(forms.ModelForm):
    """
    Formulario para la edición de una subcategoría existente.
    Incluye un campo para seleccionar la categoría padre.
    """
    categoriaPadre = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),  # Aquí defines el queryset con las opciones
        widget=forms.Select,               # Esto asegura que se renderice como un <select>
        empty_label="Seleccione una categoría",  # Etiqueta para el valor vacío
        label="Categoría Padre"            # Cambia la etiqueta si lo necesitas
    )
    class Meta:
        model = Subcategoria
        fields = '__all__'