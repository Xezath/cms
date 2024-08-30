from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')
def categorias(request):
    return render(request, 'categorias/index.html')
def crear(request):
    return render(request, 'categorias/crear.html')
def editar(request):
    return render(request, 'categorias/editar.html')