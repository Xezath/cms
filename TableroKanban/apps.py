from django.apps import AppConfig


class TablerokanbanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TableroKanban'

    def ready(self):
        import TableroKanban.signals
