from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Margenes, Color, Plantilla

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    """
    Crea datos iniciales después de la migración.

    Este receptor crea instancias de Margenes, Color y Plantilla si no existen.
    
    Args:
        sender (Model): El modelo que ha sido migrado.
        **kwargs: Argumentos adicionales proporcionados por la señal.
    """
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

            # Crear objetos Plantillas si no existen
        if not Plantilla.objects.exists():
            # Re-obteniendo los colores por si el `post_migrate` se ha ejecutado previamente
            blanco = Color.objects.get(nombre='Blanco')
            beige = Color.objects.get(nombre='Beige')
            celeste = Color.objects.get(nombre='Celeste')

            normal = Margenes.objects.get(izq=10.00)

            Plantilla.objects.create(nombre='Predeterminado', descripcion='Blanco de fondo', colorFondo=blanco, margenes=normal, disposicionHorizontal=False)
            Plantilla.objects.create(nombre='Beige', descripcion='Beige de fondo', colorFondo=beige, margenes=normal, disposicionHorizontal=False)
            Plantilla.objects.create(nombre='Cielo', descripcion='Celeste de fondo', colorFondo=celeste, margenes=normal, disposicionHorizontal=False)
