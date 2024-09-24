from django import forms
from ckeditor.widgets import CKEditorWidget
from Categoria.models import Categoria, Subcategoria
from Plantilla.models import Plantilla
from .models import Contenidos

class ContenidosForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'id': 'categoria-select'}),
        empty_label="Seleccione una categoría",
        label="Categoría"
    )
    subcategoria = forms.ModelChoiceField(
        queryset=Subcategoria.objects.none(),
        widget=forms.Select(attrs={'id': 'subcategoria-select'}),
        empty_label="Seleccione una subcategoría",
        required=False,
        label="Subcategoría"
    )
    plantilla = forms.ModelChoiceField(
        queryset=Plantilla.objects.all(),
        required=False,
        widget=forms.Select,
        empty_label="Seleccione una plantilla",
        label="Plantilla"
    )

    class Meta:
        model = Contenidos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Verificar si hay una categoría seleccionada en los datos enviados
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoriaPadre_id=categoria_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['subcategoria'].queryset = Subcategoria.objects.none()
        else:
            # Si no hay datos enviados o es una nueva instancia
            self.fields['subcategoria'].queryset = Subcategoria.objects.none()


class EditarContenidosForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'id': 'categoria-select'}),
        empty_label="Seleccione una categoría",
        label="Categoría"
    )
    subcategoria = forms.ModelChoiceField(
        queryset=Subcategoria.objects.none(),
        widget=forms.Select(attrs={'id': 'subcategoria-select'}),
        empty_label="Seleccione una subcategoría",
        required=False,
        label="Subcategoría"
    )
    plantilla = forms.ModelChoiceField(
        queryset=Plantilla.objects.all(), 
        required=False,
        widget=forms.Select,
        empty_label="Seleccione una plantilla",
        label="Plantilla"
    )

    class Meta:
        model = Contenidos
        fields = '__all__'
 
        def __init__(self, *args, **kwargs):
            
            super().__init__(*args, **kwargs)
            if 'categoria' in self.data:
                try:
                    categoria_id = int(self.data.get('categoria'))
                    self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoriaPadre_id=categoria_id).order_by('nombre')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk and self.instance.categoria:
                self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoria=self.instance.categoria).order_by('nombre')


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoria_id=categoria_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # Valor inválido de categoría, ignora y usa el queryset vacío
        elif self.instance.pk:
            self.fields['subcategoria'].queryset = self.instance.categoria.subcategorias.order_by('nombre')
