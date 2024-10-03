from django.db import models
from django.contrib.auth.models import User
from Contenidos.models import Contenidos

class Tablero(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # relacionado con el usuario que lo crea

    def __str__(self):
        return self.nombre

class Columna(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name='columnas')  # relacion uno a muchos
    orden = models.PositiveIntegerField()  # orden de la columna en el tablero

    def __str__(self):
        return f"{self.nombre} ({self.tablero.nombre})"

class Tarjeta(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('borrador', 'Borrador'),
    ]

    id = models.AutoField(primary_key=True)
    contenido = models.ForeignKey(Contenidos, on_delete=models.CASCADE)  # Relacionado con el contenido del CMS
    columna = models.ForeignKey(Columna, on_delete=models.CASCADE, related_name='tarjetas')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.PositiveIntegerField()  # Para controlar el orden de las tarjetas dentro de la columna
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')  # Nuevo campo estado

    def __str__(self):
        return f"{self.titulo} ({self.columna.nombre})"
