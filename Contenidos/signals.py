from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Estado

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'Contenidos':
        # Crear objetos Margenes si no existen
        if not Estado.objects.exists():
            Estado.objects.create(id=1, descripcion='activo')
            Estado.objects.create(id=2, descripcion='inactivo')
            Estado.objects.create(id=3, descripcion='borrador')
        