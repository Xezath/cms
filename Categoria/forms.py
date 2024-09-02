from django import forms
from .models import Categoria
from .models import Subcategoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = '__all__'

class EditarCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class EditarSubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = '__all__'