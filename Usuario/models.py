from django.db import models

# Create your models here.

# usuarios/models.py
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_migrate

#aca debo de asignar los permisos para estos roles
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == 'Usuario':  # Asegúrate de que solo se ejecuta para tu app
        groups = ['Administrador', 'Suscriptor', 'Autor', 'Editor', 'Publicador']
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)