from django.db import models

# Create your models here.
#Plantilla
class Margenes(models.Model):   #Márgenes predefinidos
    """
    Modelo para representar márgenes predefinidos.
    """
    id = models.AutoField(primary_key=True)
    """
    (AutoField): Identificador único para cada margen
    """
    der = models.DecimalField(decimal_places=2, max_digits=1000)
    """
    (DecimalField): Margen derecho
    """
    izq = models.DecimalField(decimal_places=2, max_digits=1000)
    """
    (DecimalField): Margen izquierdo
    """
    arr = models.DecimalField(decimal_places=2, max_digits=1000)
    """
    (DecimalField): Margen superior
    """
    aba = models.DecimalField(decimal_places=2, max_digits=1000)
    """
    (DecimalField): Margen inferior
    """

    def __str__(self) -> str:
        """Devuelve una representación en cadena del margen izquierdo."""
        fila = self.izq
        return str(fila)
    
class Color(models.Model):  #Colores
    """
    Modelo para representar colores.
    """
    id = models.AutoField(primary_key=True)
    """
    (AutoField): Identificador único para cada color.
    """
    nombre = models.CharField(max_length=50)
    """
    (CharField): Nombre del color.
    """
    codigo = models.CharField(max_length=50)
    """
    (CharField): Código hexadecimal del color.
    """
    def __str__(self) -> str:
        """Devuelve una representación en cadena del nombre del color."""
        fila = self.nombre
        return fila

class Plantilla(models.Model):
    """
    Modelo para representar una plantilla.
    """
    id = models.AutoField(primary_key=True)
    """
    (AutoField): Identificador único para cada plantilla.
    """
    nombre = models.CharField(max_length=50)
    """
    (CharField): Nombre de la plantilla.
    """
    descripcion = models.TextField(verbose_name="Descripcion", null=True)
    """
    (TextField): Descripción de la plantilla.
    """
    colorFondo = models.ForeignKey(Color, on_delete=models.CASCADE)
    """
    (ForeignKey): Color de fondo asociado a la plantilla.
    """
    margenes = models.ForeignKey(Margenes, on_delete=models.CASCADE)
    """
    (ForeignKey): Márgenes asociados a la plantilla.
    """
    disposicionHorizontal = models.BooleanField() #Horizonal o Vertical
    """
    (BooleanField): Indica si la disposición es horizontal o vertical.
    """

    def __str__(self):
        """Devuelve una representación en cadena del nombre de la plantilla."""
        fila = self.nombre
        return fila
    
