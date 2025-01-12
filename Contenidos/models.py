from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.models import User
from Categoria.models import Categoria, Subcategoria
from Plantilla.models import Plantilla

class Estado(models.Model):
    """
    Modelo que representa un estado de un contenido.
    """
    id = models.AutoField(primary_key=True)  # Identificador único del estado
    """
    Identificador unico del estado.
    """
    descripcion = models.CharField(max_length=50)  # Descripción del estado
    """
    Descripción del estado.
    """
    def __str__(self) -> str:
        """
        Devuelve la representación en cadena del estado.

        Returns:
            str: Descripción del estado.
        """
        return str(self.descripcion)
    

class Contenidos(models.Model):
    """
    Modelo que representa un contenido en el sistema.
    """
    titulo = models.CharField(max_length=255)  # Título del contenido
    """
    (str): El título del contenido.
    """
    contenido = RichTextField(default='')  # Contenido en formato enriquecido
    """
    (RichTextField): El contenido en formato enriquecido.
    """
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)  # Fecha de creación
    """
    (DateTimeField): La fecha de creación del contenido.
    """
    fecha_publicacion = models.DateTimeField(null=True, blank=True, editable=False)  # Fecha de publicación
    """
    (DateTimeField): Fecha en la que un contenido fue publicado
    """
    fecha_de_rechazados = models.DateTimeField(null=True, blank=True, editable=False)  # Fecha de rechazo
    """
    (DateTimeField): Fecha en la que un contenido fue rechazado
    """
    fecha_de_inactivacion = models.DateTimeField(null=True, blank=True, editable=False) # Fecha de inactivación
    """
    (DateTimeField): Fecha en la que un contenido fue puesto como inactivo
    """
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)  # Categoría asociada
    """
    (ForeignKey): La categoría asociada al contenido.
    """
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)  # Subcategoría asociada
    """
    (ForeignKey): La subcategoría asociada al contenido.
    """
    plantilla = models.ForeignKey(Plantilla, on_delete=models.SET_NULL, null=True, blank=True)  # Plantilla utilizada
    """
    (ForeignKey): La plantilla utilizada para el contenido.
    """
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Autor del contenido
    """
    (ForeignKey): El usuario que creó el contenido.
    """
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)  # Estado del contenido
    """
    (ForeignKey): El estado del contenido.
    """

    numero_lecturas = models.IntegerField(default=0, editable=False)  # Campo para el contador de lecturas
    """
    (IntegerField): Donde se cuenta el numero de visualizaciones de cada contenido
    """

    historial = models.TextField(blank=True, editable=False)
    """
    (TextField): Campo donde se almacena cada accion que se realizo sobre el contenido, desde la creacion hasta todos los estados por los que pasa
    """

    
    def agregar_historial(self, accion, detalles=""):
        """
        Agrega un registro al historial del contenido.
        """
        fecha = now().strftime("%Y-%m-%d %H:%M")
        nuevo_historial = f"{accion} - {detalles} ({fecha})\n"
        self.historial += nuevo_historial
        self.save()

    def __str__(self):
        """
        Devuelve el título del contenido.

        Returns:
            str: Título del contenido.
        """
        return self.titulo

    class Meta:
        """
        Metadatos para el modelo Contenidos.

        Permisos personalizados para la gestión de contenidos:
            can_add: Permiso para agregar contenido.
            can_modify: Permiso para editar contenido.
            can_delete: Permiso para eliminar contenido.
            can_viewInactive: Permiso para ver contenido inactivo.
        """
        permissions = [
            ("can_add", "Puede agregar contenido"),
            ("can_modify", "Puede editar contenido"),
            ("can_delete", "Puede eliminar contenido"),
            ("can_viewInactive", "Puede ver contenido inactivo"),
            ("can_viewBorrador", "Puede ver contenido en borrador"),
            ("can_viewRevision", "Puede ver contenido en revisión"),
            ("can_viewAceptado", "Puede ver contenido aceptado"),
            ("can_change_estado", "Puede cambiar estado"),
            ("can_activateContenido", "Puede activar contenido"),
            ("can_viewReportes", "Puede ver los reportes"),
        ]

class Comentario(models.Model):
    """
    Modelo que representa un comentario sobre un contenido.
    """
    comentario = models.TextField()  # Texto del comentario
    """
    (str): Texto del comentario.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el comentario con el usuario
    """
    (ForeignKey): El usuario que realizó el comentario.
    """
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del comentario
    """
    (DateTimeField): Fecha de creación del comentario.
    """
    contenido = models.ForeignKey(Contenidos, related_name='comentarios', on_delete=models.CASCADE)  # Contenido relacionado
    """
    (ForeignKey): Contenido relacionado con el comentario.
    """
    def __str__(self):
        """
        Devuelve una representación en cadena del comentario.

        Returns:
            str: Resumen del comentario que incluye el usuario y la fecha de creación.
        """
        return f'Comentario de {self.usuario} en {self.fecha_creacion}'
