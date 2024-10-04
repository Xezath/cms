from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Tablero, Columna, Estado

@receiver(post_migrate)
def create_board_columns(sender, **kwargs):
    if sender.name == 'TableroKanban':
        print("Ejecutando la señal para crear el tablero y columnas.")
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
                
            }
            for estado_nombre, estado in estados.items():
                print(f"Estado {estado_nombre}: {estado.id}")

            # Crear columnas predeterminadas si no existen
            if not Columna.objects.exists():
                Columna.objects.create(nombre='Activo', tablero=tablero, estado=estados['Activo'], orden=0)
                Columna.objects.create(nombre='Inactivo', tablero=tablero, estado=estados['Inactivo'], orden=1)
                Columna.objects.create(nombre='Borrador', tablero=tablero, estado=estados['Borrador'], orden=2)
