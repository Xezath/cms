from .models import Contenidos
from Categoria.models import Categoria, Subcategoria
from .forms import ContenidosForm, EditarContenidosForm, VisualizarContenidoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@permission_required('Contenidos.view_contenidos',raise_exception=True)
def contenidos(request):
    contenidos = Contenidos.objects.all()
    return render(request, 'contenidos/contenidos.html', {'contenidos': contenidos})

@permission_required('Contenidos.add_contenidos',raise_exception=True)
def crear_contenido(request):
    formulario = ContenidosForm(request.POST or None)
    if formulario.is_valid():
        contenidos.autor = request.user
        formulario.save()
        return redirect('contenidos')  
    return render(request, 'contenidos/crear.html', {'formulario': formulario})

@permission_required('Contenidos.change_contenidos',raise_exception=True)
def editar_contenido(request, id):
    contenido = get_object_or_404(Contenidos, id=id)

    if request.method == 'POST':
        formulario = EditarContenidosForm(request.POST, instance=contenido)
        
        # Actualiza el queryset de subcategorías basadas en la categoría seleccionada
        categoria_id = request.POST.get('categoria')
        if categoria_id:
            formulario.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoriaPadre_id=categoria_id)

        if formulario.is_valid():
            formulario.save()
            return redirect('contenidos')
        else:
            print(formulario.errors)  # Muestra los errores en la consola para depuración
    else:
        formulario = EditarContenidosForm(instance=contenido)

    return render(request, 'contenidos/editar.html', {'formulario': formulario})


@permission_required('Contenidos.delete_contenidos',raise_exception=True)
def eliminar_contenido(request, pk):
    contenido = get_object_or_404(Contenidos, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        messages.success(request, 'Contenido eliminado con éxito.')
        return redirect('contenidos')
    return render(request, 'contenidos/confirmar_eliminacion.html', {'contenido': contenido})

@permission_required('Contenidos.view_contenidos',raise_exception=True)
def visualizar_contenido(request, id):
    contenido = Contenidos.objects.get(id=id)
    formulario = VisualizarContenidoForm(request.POST or None,instance=contenido)
    if formulario.is_valid and request.POST:
        formulario.save()
    return render(request, 'contenidos/visualizar.html',{'formulario': formulario, 'contenido':contenido})

def cargar_subcategorias(request):
    categoria_id = request.GET.get('categoria_id')

    # Verificar si categoria_id es válido
    if categoria_id and categoria_id.isdigit():
        subcategorias = Subcategoria.objects.filter(categoriaPadre_id=int(categoria_id)).all()
    else:
        subcategorias = []  # Si no hay una categoría válida, devolver una lista vacía.

    return JsonResponse(list(subcategorias.values('id', 'nombre')), safe=False)
