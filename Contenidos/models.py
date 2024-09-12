from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Contenidos(models.Model):
    TIPOS_CONTENIDO = [
        ('IMG', 'Imagen'),
        ('VID', 'Video'),
        ('TXT', 'Texto'),
    ]
    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=3, choices=TIPOS_CONTENIDO)
    contenido = RichTextField(default='')
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.titulo

#permisos para realizar ciertas acciones
    class Meta:
        permissions = [
            ("can_add", "Puede agregar contenido"),
            ("can_modify", "Puede editar contenido"),
            ("can_delete", "Puede eliminar contenido"),
        ]

