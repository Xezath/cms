from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Estado

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'Contenidos':
        estados_iniciales = ['Activo', 'Inactivo', 'Borrador', 'Revision', 'Aceptado']
        for descripcion in estados_iniciales:
            Estado.objects.get_or_create(descripcion=descripcion)
