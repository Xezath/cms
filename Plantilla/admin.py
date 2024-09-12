from django.contrib import admin
from .models import Plantilla
from .models import Margenes
from .models import Color

# Register your models here.
admin.site.register(Plantilla)
admin.site.register(Margenes)
admin.site.register(Color)