from django import forms
from .models import Categoria, Subcategoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    
    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if not value:
                self.add_error(field_name, f"El campo {field_name} es obligatorio.")
        return cleaned_data

class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SubcategoriaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if not value:
                self.add_error(field_name, f"El campo {field_name} es obligatorio.")
        return cleaned_data

class EditarCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditarCategoriaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if not value:
                self.add_error(field_name, f"El campo {field_name} es obligatorio.")
        return cleaned_data

class EditarSubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditarSubcategoriaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if not value:
                self.add_error(field_name, f"El campo {field_name} es obligatorio.")
        return cleaned_data