from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para la creación de un nuevo usuario.
    Incluye campos personalizados por cada usuario
    """
    usable_password=None
    email = forms.EmailField(required=True, label="Correo Electrónico")
    class Meta:
        model = User
        fields = ( 'username','email', 'first_name', 'last_name', 'password1', 'password2')


# usuarios/forms.py
class GroupForm(forms.ModelForm):
    """
    Formulario para crear un nuevo grupo.
    Permite seleccionar múltiples permisos para el grupo.
    """
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Group  
        fields = ['name', 'permissions']  

class RoleForm(forms.Form):
    """
    Formulario para definir un nuevo rol.
    Contiene un campo para el nombre del rol.
    """
    role_name = forms.CharField(max_length=100)


class GroupEditForm(forms.ModelForm):
    """
    Formulario para editar un grupo existente.
    Permite seleccionar múltiples permisos para el grupo.
    """
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class CustomAdminUserChangeForm(UserChangeForm):
    """
    Formulario para editar un usuario existente.
    Permite seleccionar múltiples grupos para el usuario.
    """
    password = None
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Selecciona los grupos que quieres asignar al usuario.",
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups']

