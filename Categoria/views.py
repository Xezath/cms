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
def crear_cat(request):
    return render(request, 'categorias/crear.html')
def editar_cat(request):
    return render(request, 'categorias/editar.html')

#Subcategorias
def subcategorias(request):
    #subcategorias = Subcategorias.objects.all()
    #print(categorias)
    return render(request, 'subcategorias/index.html', {'subcategorias': subcategorias})
def crear_sub(request):
    return render(request, 'subcategorias/crear.html')
def editar_sub(request):
    return render(request, 'subcategorias/editar.html')
