from django.contrib import admin
from .models import Tablero, Columna, Tarjeta


# modelos importados para registrarlos en el admin
admin.site.register(Tablero)
admin.site.register(Columna)
admin.site.register(Tarjeta)
