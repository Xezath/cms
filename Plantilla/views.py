from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Plantilla
from .forms import EditarPlantillaForm, CrearPlantillaForm
from django.contrib.auth.decorators import permission_required

# Create your views here.
@permission_required('Plantilla.view_plantilla', raise_exception=True)
def plantillas(request):
    plantillas = Plantilla.objects.all()
    #print(categorias)
    return render(request, 'plantillas/index.html', {'plantillas': plantillas})

@permission_required('Plantilla.add_plantilla', raise_exception=True)
def crear_plantilla(request):
    formulario = CrearPlantillaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('/plantilla/mensajeExito_plantilla')
    return render(request, 'plantillas/crear.html', {'formulario': formulario})

@permission_required('Plantilla.change_plantilla', raise_exception=True)
def editar_plantilla(request, id):
    plantilla = Plantilla.objects.get(id=id)
    formulario = EditarPlantillaForm(request.POST or None, instance=plantilla)
    if formulario.is_valid and request.POST:
        formulario.save()
        return redirect('/plantilla/mensajeExito_plantilla')
    return render(request, 'plantillas/editar.html', {'formulario': formulario})

@permission_required('Plantilla.delete_plantilla', raise_exception=True)
def borrar_plantilla(request, id):
    plantilla = Plantilla.objects.get(id=id)
    plantilla.delete()
    return redirect('/plantilla/mensajeExito_plantilla')


def mensajeExito_plantilla(request):
    return render(request, 'plantillas/mensajeExito.html')