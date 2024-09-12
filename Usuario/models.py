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

    permisos = Permission.objects.all() #consigue todos los permisos
    
    administrador = Group.objects.get(name='Administrador') 
    for permiso in permisos: 
        administrador.permissions.add(permiso)

    autor = Group.objects.get_or_create(name='Autor')
    autor.permissions.add(Permission.objects.get(codename='add_contenidos'))

    editor = Group.objects.get_or_create(name='Autor')


    suscriptor = Group.objects.get_or_create(name='Autor')


    publicador = Group.objects.get_or_create(name='Autor')


    