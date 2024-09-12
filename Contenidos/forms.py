from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Contenidos, Categoria, Plantilla

class ContenidosForm(forms.ModelForm):
    class Meta:
        model = Contenidos
        fields = ['titulo', 'contenido', 'categoria','plantilla']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4}),
        }
        plantilla = forms.ModelChoiceField(queryset=Plantilla.objects.all(), required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()  # Cargar las categorías existentes

