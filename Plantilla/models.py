from django.db import models

# Create your models here.
#Plantilla
class Margenes(models.Model):   #Márgenes predefinidos
    id = models.AutoField(primary_key=True)
    der = models.DecimalField(decimal_places=2, max_digits=1000)
    izq = models.DecimalField(decimal_places=2, max_digits=1000)
    arr = models.DecimalField(decimal_places=2, max_digits=1000)
    aba = models.DecimalField(decimal_places=2, max_digits=1000)

    def __str__(self) -> str:
        fila = self.izq
        return str(fila)
    
class Color(models.Model):  #Colores
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)

    def __str__(self) -> str:
        fila = self.nombre
        return fila

class Plantilla(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(verbose_name="Descripcion", null=True)
    colorFondo = models.ForeignKey(Color, on_delete=models.CASCADE)
    margenes = models.ForeignKey(Margenes, on_delete=models.CASCADE)
    disposicionHorizontal = models.BooleanField() #Horizonal o Vertical

    def __str__(self):
        fila = self.nombre
        return fila
    
