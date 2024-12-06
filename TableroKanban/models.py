from django.db import models
from Contenidos.models import Contenidos, Estado
from django.contrib.auth.models import User


class Tablero(models.Model):
    """
    Modelo que representa un tablero Kanban.
    """
    id = models.AutoField(primary_key=True)
    """
    Identificador único del tablero.
    """
    nombre = models.CharField(max_length=100)
    """
    Nombre del tablero.
    """
    descripcion = models.TextField(blank=True, null=True)
    """
    Descripción opcional del tablero.
    """

    def __str__(self):
        return self.nombre


class Columna(models.Model):
    """
    Modelo que representa una columna dentro de un tablero Kanban
    """
    id = models.AutoField(primary_key=True)
    """
    Identificador único de la columna.
    """
    nombre = models.CharField(max_length=100)
    """
    Nombre de la columna
    """
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name='columnas')  # Relación uno a muchos
    """
    Relación con el tablero al que pertenece.
    """
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)  # Relaciona columna con el estado del contenido
    """
    Relación con el estado del contenido.
    """
    orden = models.PositiveIntegerField()  # Orden de la columna en el tablero
    """
    Orden de la columna en el tablero.
    """
    def __str__(self):
        return f"{self.nombre} ({self.tablero.nombre})"


class Tarjeta(models.Model):
    """
    Modelo que representa una tarjeta en una columna del tablero Kanban.
    """
    id = models.AutoField(primary_key=True)
    """
    Identificador único de la tarjeta.
    """
    contenido = models.ForeignKey(Contenidos, on_delete=models.CASCADE)  # Relacionado con el contenido del CMS
    """
    Relacionado con el contenido del CMS.
    """
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacionado con el autor del contenido
    """
    Relacionado con el autor del contenido.
    """
    columna = models.ForeignKey(Columna, on_delete=models.CASCADE, related_name='tarjetas')
    """
    Relacionado con la columna en la que se encuentra la tarjeta.
    """
    titulo = models.CharField(max_length=100)
    """
    Titulo de la tarjeta
    """
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)  # Nuevo campo de estado
    """
    Relacionado con el estado de la tarjeta.
    """
    descripcion = models.TextField(blank=True, null=True)
    """
    Descripción opcional de la tarjeta.
    """
    orden = models.PositiveIntegerField()  # Para controlar el orden de las tarjetas dentro de la columna
    """
    Orden de la tarjeta en la columna.
    """

    def save(self, *args, **kwargs):
        # Al guardar, movemos la tarjeta a la columna correcta según el estado
        """
        Método que se llama al guardar la tarjeta.

        Mueve la tarjeta a la columna correcta según el estado asociado.

        Raises:
            ValueError: Si no se encuentra una columna para el estado especificado.
        """
        if self.estado:
            try:
                # Busca la columna correspondiente al estado
                self.columna = Columna.objects.get(estado=self.estado)
            except Columna.DoesNotExist:
                raise ValueError(f"No se encontró una columna para el estado '{self.estado.descripcion}'.")
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.titulo} ({self.columna.nombre})"
    
    class Meta:
        permissions = [
            ("ver_propio_tablero", "Puede ver solo su propio contenido"),
            ("cambiar_estado_tarjeta", "Puede cambiar el estado de una tarjeta"),
        ]    
