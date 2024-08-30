from django.db import models

# Create your models here.
#Categoría
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(verbose_name="Descripcion", null=True)

    def __str__(self):
        fila = "Nombre: " + self.nombre
        return fila

#Subcategoría
class Subcategoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(verbose_name="Descripcion", null=True)
    categoriaPadre = models.ForeignKey(Categoria, related_name="subcategorias", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        fila = "Nombre: " + self.nombre
        return fila


