from django.apps import AppConfig


class ContenidosConfig(AppConfig):
    """
    Configuración de la aplicación Contenidos.

    Esta clase se encarga de definir las configuraciones específicas de la 
    aplicación 'Contenidos' dentro del proyecto CMS. Se establece el 
    tipo de campo automático para claves primarias y se importan las señales 
    necesarias para la lógica del negocio.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Contenidos'

    def ready(self):
        """
        Método que se llama cuando la aplicación está lista.

        Aquí se importan las señales definidas en la aplicación, 
        lo que permite ejecutar lógica específica en respuesta a 
        eventos de la base de datos (como crear, actualizar o eliminar objetos).
        """
        import Contenidos.signals  # Señal que crea los posibles estados
