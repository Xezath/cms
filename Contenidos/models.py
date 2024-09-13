from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User

class Plantilla(models.Model):
    nombre = models.CharField(max_length=100)
    Margenes = models.CharField(max_length=50)  # Ejemplo: '10px', '20px 30px'
    Color = models.CharField(max_length=7)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(verbose_name="Descripcion", null=True)

    def __str__(self):
        fila = self.nombre
        return fila
        
class Contenidos(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = RichTextField(default='')
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    categoria = models.ForeignKey(Categoria, related_name="contenido", blank=True, null=True, on_delete=models.CASCADE)
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