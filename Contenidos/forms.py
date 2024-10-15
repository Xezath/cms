from django import forms
from ckeditor.widgets import CKEditorWidget
from Categoria.models import Categoria, Subcategoria
from Plantilla.models import Plantilla
from .models import Contenidos, Comentario


class ContenidosForm(forms.ModelForm):
    """
    Formulario para la creación de contenidos. Incluye los campos de
    categoría, subcategoría y plantilla, con opciones dinámicas para 
    subcategorías basadas en la categoría seleccionada.
    """
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
        """
        Inicializa el formulario. Si hay datos de categoría en los datos enviados,
        se filtran las subcategorías relacionadas, de lo contrario se mantiene 
        el queryset de subcategoría vacío.
        """
        super().__init__(*args, **kwargs)
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoriaPadre_id=categoria_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['subcategoria'].queryset = Subcategoria.objects.none()
        else:
            self.fields['subcategoria'].queryset = Subcategoria.objects.none()

    def clean_contenido(self):
        """
        Valida el campo de contenido para asegurarse de que no esté vacío.
        Si está vacío, se lanza una ValidationError.
        """
        contenido = self.cleaned_data.get('contenido')
        if not contenido or contenido.strip() == '':
            raise forms.ValidationError('El campo "contenido" no puede estar vacío.')
        return contenido


class EditarContenidosForm(forms.ModelForm):
    """
    Formulario para la edición de contenidos. Incluye los campos de
    categoría, subcategoría y plantilla, con opciones dinámicas para
    subcategorías basadas en la categoría seleccionada.
    """
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'id': 'categoria-select'}),
        empty_label="Seleccione una categoría",
        label="Categoría"
    )
    subcategoria = forms.ModelChoiceField(
        queryset=Subcategoria.objects.all(),
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
        """
        Meta configuración del formulario. Especifica el modelo Contenidos y
        los campos que estarán presentes en el formulario.
        """
        model = Contenidos
        fields = ['titulo', 'contenido', 'categoria', 'subcategoria', 'estado', 'plantilla']

    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario de edición. Filtra las subcategorías dependiendo
        de la categoría seleccionada, ya sea desde los datos enviados o desde la instancia existente.
        """
        super().__init__(*args, **kwargs)
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoriaPadre_id=categoria_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.categoria:
            self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoriaPadre=self.instance.categoria).order_by('nombre')


class VisualizarContenidoForm(forms.ModelForm):
    """
    Formulario para la visualización de contenidos. Se utiliza para mostrar
    los datos sin opción de modificación.
    """
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
        """
        Inicializa el formulario de visualización. Filtra las subcategorías
        dependiendo de la categoría seleccionada en los datos o instancia actual.
        """
        super().__init__(*args, **kwargs)
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoria_id=categoria_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # Valor inválido de categoría, ignora y usa el queryset vacío
        elif self.instance.pk:
            self.fields['subcategoria'].queryset = self.instance.categoria.subcategorias.order_by('nombre')


class ComentarioForm(forms.ModelForm):
    """
    Formulario para la creación de comentarios. Solo incluye el campo 'comentario'.
    """
    class Meta:
        """
        Meta configuración del formulario. Especifica el modelo Comentario y
        que solo el campo 'comentario' estará presente en el formulario.
        """
        model = Comentario
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu comentario aquí...'}),
        }
        labels = {
            'comentario': '',
        }
