from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User
from Categoria.models import Categoria, Subcategoria
from Plantilla.models import Plantilla

class Estado(models.Model):
    """
    Modelo que representa un estado de un contenido.

    Atributos:
        id (int): Identificador único del estado.
        descripcion (str): Descripción del estado.
    """
    id = models.AutoField(primary_key=True)  # Identificador único del estado
    descripcion = models.CharField(max_length=50)  # Descripción del estado

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

    Atributos:
        titulo (str): El título del contenido.
        contenido (RichTextField): El contenido en formato enriquecido.
        fecha_creacion (DateTimeField): La fecha de creación del contenido.
        categoria (ForeignKey): La categoría asociada al contenido.
        subcategoria (ForeignKey): La subcategoría asociada al contenido.
        plantilla (ForeignKey): La plantilla utilizada para el contenido.
        autor (ForeignKey): El usuario que creó el contenido.
        estado (ForeignKey): El estado del contenido.
    """
    titulo = models.CharField(max_length=255)  # Título del contenido
    contenido = RichTextField(default='')  # Contenido en formato enriquecido
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)  # Fecha de creación
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)  # Categoría asociada
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)  # Subcategoría asociada
    plantilla = models.ForeignKey(Plantilla, on_delete=models.SET_NULL, null=True, blank=True)  # Plantilla utilizada
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Autor del contenido
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)  # Estado del contenido

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
        ]

class Comentario(models.Model):
    """
    Modelo que representa un comentario sobre un contenido.

    Atributos:
        comentario (str): Texto del comentario.
        usuario (ForeignKey): El usuario que realizó el comentario.
        fecha_creacion (DateTimeField): Fecha de creación del comentario.
        contenido (ForeignKey): Contenido relacionado con el comentario.
    """
    comentario = models.TextField()  # Texto del comentario
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el comentario con el usuario
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del comentario
    contenido = models.ForeignKey(Contenidos, related_name='comentarios', on_delete=models.CASCADE)  # Contenido relacionado

    def __str__(self):
        """
        Devuelve una representación en cadena del comentario.

        Returns:
            str: Resumen del comentario que incluye el usuario y la fecha de creación.
        """
        return f'Comentario de {self.usuario} en {self.fecha_creacion}'
