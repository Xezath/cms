from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Categoria
from .models import Subcategoria
from .forms import CategoriaForm, SubcategoriaForm, EditarCategoriaForm, EditarSubcategoriaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

# Create your views here.
@login_required
def inicio(request):
    """
    Renderiza la página de inicio del sistema.
    """
    return render(request, 'paginas/inicio.html')

@permission_required('Categoria.view_categoria', raise_exception=True)
def categorias(request):
    """
    Muestra la lista de categorías disponibles en el sistema.
    Requiere el permiso 'view_categoria'.
    
    Argumentos:
    - request: Solicitud HTTP.
    """
    categorias = Categoria.objects.all()
    #print(categorias)
    return render(request, 'categorias/index.html', {'categorias': categorias})

@permission_required('Categoria.add_categoria', raise_exception=True)
def crear_cat(request):
    """
    Vista para crear una nueva categoría.
    Requiere el permiso 'add_categoria'.
    
    Argumentos:
    - request: Solicitud HTTP.
    """
    formulario = CategoriaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('/categoria/mensajeExito')
    return render(request, 'categorias/crear.html', {'formulario': formulario})

@permission_required('Categoria.change_categoria', raise_exception=True)
def editar_cat(request, id):
    """
    Vista para editar una categoría existente.
    Requiere el permiso 'change_categoria'.
    
    Argumentos:
    - request: Solicitud HTTP.
    - id: Identificador de la categoría a editar.
    """
    categoria = Categoria.objects.get(id=id)
    formulario = EditarCategoriaForm(request.POST or None, instance=categoria)
    if formulario.is_valid and request.POST:
        formulario.save()
        return redirect('/categoria/mensajeExito')
    return render(request, 'categorias/editar.html', {'formulario': formulario})

@permission_required('Categoria.delete_categoria', raise_exception=True)
def borrar_cat(request, id):
    """
    Vista para eliminar una categoría.
    Requiere el permiso 'delete_categoria'.
    
    Argumentos:
    - request: Solicitud HTTP.
    - id: Identificador de la categoría a eliminar.
    """
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('/categoria/mensajeExito')

#Subcategorias
@permission_required('Categoria.view_subcategoria', raise_exception=True)
def subcategorias(request):
    """
    Muestra la lista de subcategorías disponibles en el sistema.
    Requiere el permiso 'view_subcategoria'.
    
    Argumentos:
    - request: Solicitud HTTP.
    """
    subcategorias = Subcategoria.objects.all()
    #print(subcategorias)
    return render(request, 'subcategorias/index.html', {'subcategorias': subcategorias})

@permission_required('Categoria.add_subcategoria', raise_exception=True)
def crear_sub(request):
    """
    Vista para crear una nueva subcategoría.
    Requiere el permiso 'add_subcategoria'.
    
    Argumentos:
    - request: Solicitud HTTP.
    """
    formulario = SubcategoriaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('/categoria/mensajeExito_sub')
    return render(request, 'subcategorias/crear.html', {'formulario': formulario})

@permission_required('Categoria.change_subcategoria', raise_exception=True)
def editar_sub(request, id):
    """
    Vista para editar una subcategoría existente.
    Requiere el permiso 'change_subcategoria'.
    
    Argumentos:
    - request: Solicitud HTTP.
    - id: Identificador de la subcategoría a editar.
    """
    subcategoria = Subcategoria.objects.get(id=id)
    formulario = EditarSubcategoriaForm(request.POST or None, instance=subcategoria)
    if formulario.is_valid and request.POST:
        formulario.save()
        return redirect('/categoria/mensajeExito_sub')
    return render(request, 'subcategorias/editar.html', {'formulario': formulario})

@permission_required('Categoria.delete_subcategoria', raise_exception=True)
def borrar_sub(request, id):
    """
    Vista para eliminar una subcategoría.
    Requiere el permiso 'delete_subcategoria'.
    
    Argumentos:
    - request: Solicitud HTTP.
    - id: Identificador de la subcategoría a eliminar.
    """
    subcategoria = Subcategoria.objects.get(id=id)
    subcategoria.delete()
    return redirect('/categoria/mensajeExito_sub')

#Exito de cambios
def mensajeExito(request):
    """
    Muestra un mensaje de éxito después de completar una operación sobre categorías.
    
    Argumentos:
    - request: Solicitud HTTP.
    """
    return render(request, 'categorias/mensajeExito.html')

def mensajeExito_sub(request):
    """
    Muestra un mensaje de éxito después de completar una operación sobre subcategorías.
    
    Argumentos:
    - request: Solicitud HTTP.
    """
    return render(request, 'subcategorias/mensajeExito.html')