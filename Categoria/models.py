from django.db import models

# Create your models here.
#Categoría
class Categoria(models.Model):
    """
    Modelo que representa una categoría de contenido.
    """
    id = models.AutoField(primary_key=True)
    """
    Identificador único de la categoría.
    """
    nombre = models.CharField(max_length=50)
    """
    Nombre de la categoría.
    """
    descripcion = models.TextField(verbose_name="Descripcion", null=True)
    """
     Descripción detallada de la categoría.
    """

    def __str__(self):
        """
        Retorna el nombre de la categoría.
        """
        fila = self.nombre
        return fila

#Subcategoría
class Subcategoria(models.Model):
    """
    Modelo que representa una subcategoría de una categoría principal.
    """
    id = models.AutoField(primary_key=True)
    """
    Identificador unico de la subcategoria
    """
    nombre = models.CharField(max_length=100)
    """
    Nombre de la subcategoria
    """
    descripcion = models.TextField(verbose_name="Descripcion", null=True)
    """
    Descripcion detallada de la subcategoria
    """
    categoriaPadre = models.ForeignKey(Categoria, related_name="subcategorias", blank=True, null=True, on_delete=models.CASCADE)
    """
    Relacion con la categoria principal a la que pertenece
    """
    def __str__(self):
        """
        Retorna el nombre de la subcategoría.
        """
        fila = self.nombre
        return fila


