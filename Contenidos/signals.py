from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Estado

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    """
    Crea los estados iniciales ('Activo', 'Inactivo', 'Borrador') en la tabla Estado
    después de la migración de la aplicación 'Contenidos', si estos no existen.
    
    Args:
        sender (AppConfig): La aplicación que envía la señal.
        **kwargs: Argumentos adicionales que pueden ser pasados en la señal.
    """
    if sender.name == 'Contenidos':
        # Crear objetos Margenes si no existen
        if not Estado.objects.exists():
            Estado.objects.create(id=1, descripcion='Activo')
            Estado.objects.create(id=2, descripcion='Inactivo')
            Estado.objects.create(id=3, descripcion='Borrador')
            Estado.objects.create(id=4, descripcion='Revision')
            Estado.objects.create(id=5, descripcion='Rechazado')
        