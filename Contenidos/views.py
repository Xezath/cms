from .models import Contenidos, Categoria
from .forms import ContenidosForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required
def contenidos(request):
    contenidos = Contenidos.objects.all()
    return render(request, 'contenidos/contenidos.html', {'contenidos': contenidos})

@permission_required('Contenidos.add_contenidos',raise_exception=True)
def crear_contenido(request):
    formulario = ContenidosForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('contenidos') 
    return render(request, 'contenidos/crear.html', {'formulario': formulario})


#@permission_required('Contenidos.can_modify', raise_exception=True)
def editar_contenido(request, pk):
    contenido = get_object_or_404(Contenidos, pk=pk)
    if request.method == 'POST':
        form = ContenidosForm(request.POST, instance=contenido)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contenido actualizado con éxito.')
            return redirect('contenidos')  # Redirige a la lista de contenidos
    else:
        form = ContenidosForm(instance=contenido)
    return render(request, 'contenidos/editar.html', {'form': form})


#@permission_required('Contenidos.can_delete', raise_exception=True)
def eliminar_contenido(request, pk):
    contenido = get_object_or_404(Contenidos, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        messages.success(request, 'Contenido eliminado con éxito.')
        return redirect('contenidos')  # Redirige a la lista de contenidos
    return render(request, 'contenidos/confirmar_eliminacion.html', {'contenido': contenido})
