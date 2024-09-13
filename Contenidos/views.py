from .models import Contenidos
from .forms import ContenidosForm, EditarContenidosForm, VisualizarContenidoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def contenidos(request):
    contenidos = Contenidos.objects.all()
    return render(request, 'contenidos/contenidos.html', {'contenidos': contenidos})

def crear_contenido(request):
    formulario = ContenidosForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('contenidos')  
    return render(request, 'contenidos/crear.html', {'formulario': formulario})

def editar_contenido(request, id):
    contenido = Contenidos.objects.get(id=id)
    formulario = EditarContenidosForm(request.POST or None,instance=contenido)
    if formulario.is_valid and request.POST:
        formulario.save()
        return redirect('contenidos')
    return render(request, 'contenidos/editar.html',{'formulario': formulario, 'contenido':contenido})

def eliminar_contenido(request, pk):
    contenido = get_object_or_404(Contenidos, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        messages.success(request, 'Contenido eliminado con éxito.')
        return redirect('contenidos')
    return render(request, 'contenidos/confirmar_eliminacion.html', {'contenido': contenido})

def visualizar_contenido(request, id):
    contenido = Contenidos.objects.get(id=id)
    formulario = VisualizarContenidoForm(request.POST or None,instance=contenido)
    if formulario.is_valid and request.POST:
        formulario.save()
    return render(request, 'contenidos/visualizar.html',{'formulario': formulario, 'contenido':contenido})
