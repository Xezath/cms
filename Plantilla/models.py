from django.db import models

# Create your models here.
#Plantilla
class Tipografia(models.Model):
    id = models.AutoField(primary_key=True)
    estilo = models.CharField(max_length=50)
    def __str__(self) -> str:
        fila = self.estilo
        return fila

class Margenes(models.Model):   #Márgenes predefinidos
    id = models.AutoField(primary_key=True)
    der = models.DecimalField(decimal_places=2, max_digits=1000)
    izq = models.DecimalField(decimal_places=2, max_digits=1000)
    arr = models.DecimalField(decimal_places=2, max_digits=1000)
    aba = models.DecimalField(decimal_places=2, max_digits=1000)

    def __str__(self) -> str:
        fila = self.izq
        return str(fila)

class Modulos(models.Model):    #Módulos multimedia
    id = models.AutoField(primary_key=True)
    tipoMultimedia = models.CharField(max_length=50)

    def __str__(self) -> str:
        fila = self.tipoMultimedia
        return fila
    
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
    tipografia = models.ForeignKey(Tipografia, on_delete=models.CASCADE)
    margenes = models.ForeignKey(Margenes, on_delete=models.CASCADE)
    disposicionHorizontal = models.BooleanField() #Horizonal o Vertical
    modulos = models.ForeignKey(Modulos, on_delete=models.CASCADE)

    def __str__(self):
        fila = self.nombre
        return fila
    
