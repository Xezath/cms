from django.contrib import admin
from .models import Plantilla
from .models import Tipografia
from .models import Margenes
from .models import Modulos

# Register your models here.
admin.site.register(Plantilla)
admin.site.register(Tipografia)
admin.site.register(Margenes)
admin.site.register(Modulos)