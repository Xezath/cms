from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria, Subcategoria

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    """
    Crea datos iniciales de categorías y subcategorías tras la migración de la base de datos.
    
    Se ejecuta después de la migración de la aplicación e inserta datos en las tablas
    de categorías y subcategorías si estas no tienen datos.
    
    Argumentos:
    - sender: La aplicación que ha sido migrada.
    """
    # Verificar si el modelo que se está migrando es el correcto
    if sender.name == 'Categoria':  # Reemplaza 'your_app_name' con el nombre de tu aplicación
        # Crear objetos Categorias si no existen
        if not Categoria.objects.exists():
            cine = Categoria.objects.create(nombre='Cine', descripcion='Peliculas y series de televisión.')
            musica = Categoria.objects.create(nombre='Música', descripcion='Albumes, canciones y artistas musicales.')
            videojuegos = Categoria.objects.create(nombre='Videojuegos', descripcion='Todo sobre juegos digitales.')
            entretenimiento = Categoria.objects.create(nombre='Entretenimiento', descripcion='Entretenimientos generales.')

        # Crear objetos Subcategorias si no existen
        if not Subcategoria.objects.exists():
            # Re-obteniendo las categorías por si el `post_migrate` se ha ejecutado previamente
            cine = Categoria.objects.get(nombre='Cine')
            musica = Categoria.objects.get(nombre='Música')
            videojuegos = Categoria.objects.get(nombre='Videojuegos')
            entretenimiento = Categoria.objects.get(nombre='Entretenimiento')

            Subcategoria.objects.create(nombre='Trailers', descripcion='Trailers de peliculas y series de televisión.', categoriaPadre=cine)
            Subcategoria.objects.create(nombre='Cantantes', descripcion='Artistas musicales.', categoriaPadre=musica)
            Subcategoria.objects.create(nombre='Genshin Impact', descripcion='Todo sobre juegos genshin impact.', categoriaPadre=videojuegos)
            Subcategoria.objects.create(nombre='Famosos', descripcion='Mundo de la fama.', categoriaPadre=entretenimiento)
