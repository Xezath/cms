from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User
from Categoria.models import Categoria
from Plantilla.models import Plantilla
        
class Contenidos(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = RichTextField(default='')
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titulo

#permisos para realizar ciertas acciones
    class Meta:
        permissions = [
            ("can_add", "Puede agregar contenido"),
            ("can_modify", "Puede editar contenido"),
            ("can_delete", "Puede eliminar contenido"),
        ]

