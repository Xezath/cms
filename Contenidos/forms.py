from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Contenidos, Categoria

class ContenidosForm(forms.ModelForm):
    class Meta:
        model = Contenidos
        fields = ['titulo', 'tipo', 'contenido', 'categoria']
        widgets = {
            'tipo': forms.Select(choices=Contenidos.TIPOS_CONTENIDO),
            'contenido': forms.Textarea(attrs={'rows': 4}),
        }

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()  # Cargar las categorías existentes
