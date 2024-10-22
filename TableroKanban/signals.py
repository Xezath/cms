from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Tablero, Columna, Estado

@receiver(post_migrate)
def create_board_columns(sender, **kwargs):
    """
    Crea un tablero y columnas predeterminadas después de migraciones.

    Args:
        sender: La aplicación que envió la señal.
    """
    if sender.name == 'TableroKanban':
        # Crear un tablero predeterminado si no existe
        if not Tablero.objects.exists():
            tablero = Tablero.objects.create(
                nombre='Tablero Kanban',
                descripcion='Tablero Kanban predeterminado.'
            )

            # Crear estados predeterminados si no existen
            estados = {
                'Activo': Estado.objects.get_or_create(descripcion='Activo')[0],
                'Inactivo': Estado.objects.get_or_create(descripcion='Inactivo')[0],
                'Borrador': Estado.objects.get_or_create(descripcion='Borrador')[0],
                'Revision': Estado.objects.get_or_create(descripcion='Revision')[0],
                'Aceptado': Estado.objects.get_or_create(descripcion='Aceptado')[0]
            }

            # Crear columnas predeterminadas si no existen
            if not Columna.objects.exists():
                Columna.objects.create(nombre='Activo', tablero=tablero, estado=estados['Activo'], orden=0)
                Columna.objects.create(nombre='Inactivo', tablero=tablero, estado=estados['Inactivo'], orden=1)
                Columna.objects.create(nombre='Borrador', tablero=tablero, estado=estados['Borrador'], orden=2)
                Columna.objects.create(nombre='Revision', tablero=tablero, estado=estados['Revision'], orden=3)
                Columna.objects.create(nombre='Aceptado', tablero=tablero, estado=estados['Aceptado'], orden=4)

