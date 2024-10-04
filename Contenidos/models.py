from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User
from Categoria.models import Categoria,Subcategoria
from Plantilla.models import Plantilla
    
class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
        
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
    """
    titulo = models.CharField(max_length=255)
    contenido = RichTextField(default='')
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.SET_NULL, null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

#permisos para realizar ciertas acciones
    class Meta:
        permissions = [
            ("can_add", "Puede agregar contenido"),
            ("can_modify", "Puede editar contenido"),
            ("can_delete", "Puede eliminar contenido"),
        ]

class Comentario(models.Model):
    """
    Modelo que representa un comentario sobre un contenido.
    """
    comentario = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el comentario con el usuario
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    contenido = models.ForeignKey(Contenidos, related_name='comentarios', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comentario de {self.usuario} en {self.fecha_creacion}'
