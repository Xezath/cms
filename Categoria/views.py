from django.shortcuts import render
from django.http import HttpResponse
from .models import Categoria
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')
def categorias(request):
    categorias = Categoria.objects.all()
    #print(categorias)
    return render(request, 'categorias/index.html', {'categorias': categorias})
def crear(request):
    return render(request, 'categorias/crear.html')
def editar(request):
    return render(request, 'categorias/editar.html')