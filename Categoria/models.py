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

#Plantilla
class Tipografia(models.Model):
    id = models.AutoField(primary_key=True)
    estilo = models.CharField(max_length=50)

class Margenes(models.Model):   #Márgenes predefinidos
    id = models.AutoField(primary_key=True)
    der = models.DecimalField(decimal_places=2, max_digits=1000)
    izq = models.DecimalField(decimal_places=2, max_digits=1000)
    arr = models.DecimalField(decimal_places=2, max_digits=1000)
    aba = models.DecimalField(decimal_places=2, max_digits=1000)

class Modulos(models.Model):    #Módulos multimedia
    id = models.AutoField(primary_key=True)
    tipoMultimedia = models.CharField(max_length=50)

class Plantilla(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(verbose_name="Descripcion", null=True)
    colorFondo = models.IntegerField()
    tipografia = models.ForeignKey(Tipografia, on_delete=models.CASCADE)
    margenes = models.ForeignKey(Margenes, on_delete=models.CASCADE)
    disposicion = models.BooleanField() #Horizonal o Vertical
    modulos = models.ForeignKey(Modulos, on_delete=models.CASCADE)

    def __str__(self):
        fila = "Nombre: " + self.nombre
        return fila

