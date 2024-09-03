from django.contrib import admin
from .models import Categoria
from .models import Subcategoria

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Subcategoria)