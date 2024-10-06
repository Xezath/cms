from django.db import models
from Contenidos.models import Contenidos, Estado
from django.contrib.auth.models import User


class Tablero(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Columna(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name='columnas')  # Relación uno a muchos
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)  # Relaciona columna con el estado del contenido
    orden = models.PositiveIntegerField()  # Orden de la columna en el tablero

    def __str__(self):
        return f"{self.nombre} ({self.tablero.nombre})"


class Tarjeta(models.Model):
    id = models.AutoField(primary_key=True)
    contenido = models.ForeignKey(Contenidos, on_delete=models.CASCADE)  # Relacionado con el contenido del CMS
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacionado con el autor del contenido
    columna = models.ForeignKey(Columna, on_delete=models.CASCADE, related_name='tarjetas')
    titulo = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)  # Nuevo campo de estado
    descripcion = models.TextField(blank=True, null=True)
    orden = models.PositiveIntegerField()  # Para controlar el orden de las tarjetas dentro de la columna

    def save(self, *args, **kwargs):
        # Al guardar, movemos la tarjeta a la columna correcta según el estado
        if self.estado:
            try:
                # Busca la columna correspondiente al estado
                self.columna = Columna.objects.get(estado=self.estado)
            except Columna.DoesNotExist:
                raise ValueError(f"No se encontró una columna para el estado {self.estado}.")
        
        super(Tarjeta, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} ({self.columna.nombre})"
    
    class Meta:
        permissions = [
            ("ver_propio_tablero", "Puede ver solo su propio contenido"),
        ]    
