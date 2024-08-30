from django.shortcuts import render
from django.http import HttpResponse
from .models import Plantilla

# Create your views here.
def plantillas(request):
    plantillas = Plantilla.objects.all()
    #print(categorias)
    return render(request, 'plantillas/index.html', {'plantillas': plantillas})
def crear(request):
    return render(request, 'plantillas/crear.html')
def editar(request):
    return render(request, 'plantillas/editar.html')