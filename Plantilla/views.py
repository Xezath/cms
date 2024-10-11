from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Plantilla
from .forms import EditarPlantillaForm, CrearPlantillaForm
from django.contrib.auth.decorators import permission_required

# Create your views here.
@permission_required('Plantilla.view_plantilla', raise_exception=True)
def plantillas(request):
    """
    Vista que muestra todas las plantillas.

    Esta vista renderiza la plantilla 'index.html' y pasa una lista 
    de todas las plantillas disponibles.

    Args:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Returns:
        HttpResponse: La respuesta con la renderización de la plantilla.
    """
    plantillas = Plantilla.objects.all()
    #print(categorias)
    return render(request, 'plantillas/index.html', {'plantillas': plantillas})

@permission_required('Plantilla.add_plantilla', raise_exception=True)
def crear_plantilla(request):
    """
    Vista para crear una nueva plantilla.

    Esta vista renderiza un formulario para crear una nueva plantilla. 
    Si el formulario es válido, guarda la plantilla y redirige al usuario.

    Args:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Returns:
        HttpResponse: La respuesta con la renderización del formulario 
        o una redirección después de guardar la plantilla.
    """
    formulario = CrearPlantillaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('/plantilla/mensajeExito_plantilla')
    return render(request, 'plantillas/crear.html', {'formulario': formulario})

@permission_required('Plantilla.change_plantilla', raise_exception=True)
def editar_plantilla(request, id):
    """
    Vista para editar una plantilla existente.

    Esta vista carga una plantilla existente y renderiza un formulario 
    para editarla. Si el formulario es válido, guarda los cambios y redirige.

    Args:
        request (HttpRequest): El objeto de la solicitud HTTP.
        id (int): El identificador de la plantilla a editar.

    Returns:
        HttpResponse: La respuesta con la renderización del formulario 
        o una redirección después de guardar los cambios.
    """
    plantilla = Plantilla.objects.get(id=id)
    formulario = EditarPlantillaForm(request.POST or None, instance=plantilla)
    if formulario.is_valid and request.POST:
        formulario.save()
        return redirect('/plantilla/mensajeExito_plantilla')
    return render(request, 'plantillas/editar.html', {'formulario': formulario})

@permission_required('Plantilla.delete_plantilla', raise_exception=True)
def borrar_plantilla(request, id):
    """
    Vista para borrar una plantilla.

    Esta vista elimina la plantilla identificada por su id y redirige 
    al usuario a una página de éxito.

    Args:
        request (HttpRequest): El objeto de la solicitud HTTP.
        id (int): El identificador de la plantilla a borrar.

    Returns:
        HttpResponse: La respuesta que redirige al usuario después de borrar la plantilla.
    """
    plantilla = Plantilla.objects.get(id=id)
    plantilla.delete()
    return redirect('/plantilla/mensajeExito_plantilla')


def mensajeExito_plantilla(request):
    """
    Vista que muestra un mensaje de éxito.

    Esta vista renderiza una plantilla que muestra un mensaje de 
    éxito después de realizar una acción en las plantillas.

    Args:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Returns:
        HttpResponse: La respuesta con la renderización de la plantilla de éxito.
    """
    return render(request, 'plantillas/mensajeExito.html')