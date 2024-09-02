from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    usable_password=None
    email = forms.EmailField(required=True, label="Correo Electrónico")
    class Meta:
        model = User
        fields = ( 'username','email', 'first_name', 'last_name', 'password1', 'password2')