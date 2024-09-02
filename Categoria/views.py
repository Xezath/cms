from django.shortcuts import render
from django.http import HttpResponse
from .models import Categoria
from .models import Subcategoria
from .forms import CategoriaForm, SubcategoriaForm, EditarCategoriaForm, EditarSubcategoriaForm
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')
def categorias(request):
    categorias = Categoria.objects.all()
    #print(categorias)
    return render(request, 'categorias/index.html', {'categorias': categorias})
def crear_cat(request):
    formulario = CategoriaForm(request.POST or None)
    return render(request, 'categorias/crear.html', {'formulario': formulario})
def editar_cat(request):
    formulario = EditarCategoriaForm(request.POST or None)
    return render(request, 'categorias/editar.html', {'formulario': formulario})

#Subcategorias
def subcategorias(request):
    subcategorias = Subcategoria.objects.all()
    #print(subcategorias)
    return render(request, 'subcategorias/index.html', {'subcategorias': subcategorias})
def crear_sub(request):
    formulario = SubcategoriaForm(request.POST or None)
    return render(request, 'subcategorias/crear.html', {'formulario': formulario})
def editar_sub(request):
    formulario = EditarSubcategoriaForm(request.POST or None)
    return render(request, 'subcategorias/editar.html', {'formulario': formulario})
