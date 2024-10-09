from django.apps import AppConfig


class CategoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Categoria'
    
    def ready(self):
        import Categoria.signals  # Señal que crea los posibles estados