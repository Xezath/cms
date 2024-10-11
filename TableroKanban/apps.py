from django.apps import AppConfig


class TablerokanbanConfig(AppConfig):
    """
    Configuración de la aplicación TableroKanban.

    Attributes:
        default_auto_field: El campo de auto-incremento predeterminado.
        name: El nombre de la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TableroKanban'

    def ready(self):
        import TableroKanban.signals
