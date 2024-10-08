from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group


class CustomUserCreationForm(UserCreationForm):
    usable_password=None
    email = forms.EmailField(required=True, label="Correo Electrónico")
    class Meta:
        model = User
        fields = ( 'username','email', 'first_name', 'last_name', 'password1', 'password2')


# usuarios/forms.py
class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Group  
        fields = ['name', 'permissions']  

class RoleForm(forms.Form):
    role_name = forms.CharField(max_length=100)


class GroupEditForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class CustomAdminUserChangeForm(UserChangeForm):
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

