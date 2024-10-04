from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Margenes, Color

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'Plantilla':
        # Crear objetos Margenes si no existen
        if not Margenes.objects.exists():
            Margenes.objects.create(der=10.00, izq=10.00, arr=10.00, aba=10.00)
            Margenes.objects.create(der=20.00, izq=20.00, arr=20.00, aba=20.00)
        
        # Crear objetos Color si no existen
        if not Color.objects.exists():
            Color.objects.create(nombre='Blanco', codigo='#ffffff')
            Color.objects.create(nombre='Beige', codigo='#f5f5dc')
            Color.objects.create(nombre='Celeste', codigo='#00eaff')
