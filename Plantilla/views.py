from django.shortcuts import render
from django.http import HttpResponse
from .models import Plantilla
from .forms import EditarPlantillaForm, CrearPlantillaForm

# Create your views here.
def plantillas(request):
    plantillas = Plantilla.objects.all()
    #print(categorias)
    return render(request, 'plantillas/index.html', {'plantillas': plantillas})
def crear_plantilla(request):
    formulario = CrearPlantillaForm(request.POST or None)
    return render(request, 'plantillas/crear.html', {'formulario': formulario})
def editar_plantilla(request):
    formulario = EditarPlantillaForm(request.POST or None)
    return render(request, 'plantillas/editar.html', {'formulario': formulario})