from django.apps import AppConfig


class ContenidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Contenidos'

    def ready(self):
        import Contenidos.signals  # Señal que crea los posibles estados
