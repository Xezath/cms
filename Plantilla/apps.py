from django.apps import AppConfig


class PlantillaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Plantilla'

    def ready(self):
        import Plantilla.signals  # Asegúrate de que 'tu_app_name' es correcto
