from .models import Contenidos, Comentario, Estado
from Categoria.models import Categoria, Subcategoria
from .forms import ContenidosForm, EditarContenidosForm, VisualizarContenidoForm, ComentarioForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.models import User, Permission
from TableroKanban.models import Tablero, Tarjeta
from django.db.models import Q
from TableroKanban.views import actualizar_estado
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from datetime import datetime

@permission_required('Contenidos.view_contenidos', raise_exception=True)
def contenidos(request):
    """
    Muestra una lista de todos los contenidos disponibles, permitiendo filtrarlos por categoría, 
    subcategoría o autor. También carga las listas necesarias para realizar los filtros.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.

    Retorna:
    - HttpResponse con la página 'contenidos/contenidos.html', que incluye la lista de contenidos y los filtros.
    """
    # Obtener los parámetros de filtrado de la solicitud
    categoria_id = request.GET.get('categoria')
    subcategoria_id = request.GET.get('subcategoria')
    autor_id = request.GET.get('autor')
    # Filtrar contenidos basado en los parámetros
    contenidos = Contenidos.objects.all()

    if categoria_id:
        contenidos = contenidos.filter(categoria_id=categoria_id)
    
    if subcategoria_id:
        contenidos = contenidos.filter(subcategoria_id=subcategoria_id)
    
    if autor_id:
        contenidos = contenidos.filter(autor_id=autor_id)
    # Obtener listas para los filtros
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()
    permiso_crear_contenido = Permission.objects.get(codename='add_contenidos')
    autores = User.objects.filter(
        Q(user_permissions=permiso_crear_contenido) | 
        Q(groups__permissions=permiso_crear_contenido)
    ).distinct()

    return render(request, 'contenidos/contenidos.html', {
        'contenidos': contenidos,
        'categorias': categorias,
        'subcategorias': subcategorias,
        'autores': autores
    })

@permission_required('Contenidos.add_contenidos', raise_exception=True)
def crear_contenido(request):
    """
    Vista para crear un nuevo contenido. Una vez creado, se asocia una tarjeta en el tablero Kanban 
    al contenido creado.

    Esta accion es agregada al historial del contenido con el estado inicial que se seleccionó.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.

    Retorna:
    - HttpResponse que redirige a la lista de contenidos si se crea con éxito o muestra la página 'contenidos/crear.html' con el formulario si no es válido.
    """
    formulario = ContenidosForm(request.POST or None)
    
    if formulario.is_valid():
        contenido = formulario.save(commit=False)  # Guarda el contenido, pero no en la base de datos todavía
        contenido.autor = request.user  # Asigna el autor al contenido
        contenido.save()  # Guarda el contenido en la base de datos

        # Registrar el estado inicial en el historial
        contenido.agregar_historial(
            "Creado",
            f"El contenido ha sido creado y se encuentra en estado '{contenido.estado.descripcion}'."
        )

        tablero = Tablero.objects.first()  # Obtener el tablero por defecto

        # Buscar la columna que coincida con el estado del contenido recién creado
        columna_correspondiente = tablero.columnas.filter(estado=contenido.estado).first()

        if not columna_correspondiente:
            raise ValueError(f"No se encontró una columna para el estado {contenido.estado.descripcion}.")

        # Crear una tarjeta asociada al contenido recién creado
        Tarjeta.objects.create(
            contenido=contenido,
            autor=request.user,
            columna=columna_correspondiente,
            titulo=contenido.titulo,  # Usa el título del contenido
            estado=contenido.estado,
            descripcion=contenido.autor,  
            orden=0,  # Establecer un orden inicial
        )
        return redirect('visualizar_contenido_borrador', contenido.id)
    
    # Si el formulario no es válido, se vuelve a mostrar con los errores
    return render(request, 'contenidos/crear.html', {'formulario': formulario})



#@permission_required('Contenidos.change_contenidos', raise_exception=True)
@login_required
def editar_contenido(request, id):
    """
    Vista para editar un contenido existente. También actualiza la tarjeta asociada en el tablero Kanban si el estado del contenido cambia.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - id: ID del contenido a editar.

    Retorna:
    - HttpResponse que redirige a la lista de contenidos si la edición se completa con éxito, o muestra la página 'contenidos/editar.html' con el formulario si no es válido.
    
    Esta accion es agregada al historial del contenido.
    """
    contenido = get_object_or_404(Contenidos, id=id)
    estado_anterior= contenido.estado
    tarjeta = Tarjeta.objects.filter(contenido=contenido).first()  # Buscar la tarjeta relacionada con el contenido

    if request.method == 'POST':
        formulario = EditarContenidosForm(request.POST, instance=contenido)

        # Actualiza el queryset de subcategorías basadas en la categoría seleccionada
        categoria_id = request.POST.get('categoria')
        if categoria_id:
            formulario.fields['subcategoria'].queryset = Subcategoria.objects.filter(categoriaPadre_id=categoria_id)

        if formulario.is_valid():
            # Aquí no es necesario modificar el autor
            contenido = formulario.save(commit=False)  # No guardar aún
            contenido.autor = contenido.autor  # Mantener el autor existente
            if contenido.estado.id == 2:
                contenido.fecha_de_inactivacion = datetime.now()

            if contenido.estado.id == 1:
                contenido.fecha_publicacion = datetime.now()

            contenido.save()  # Guarda el contenido modificado
            contenido.agregar_historial("Modificado", "El contenido ha sido modificado.")
            
            nuevo_estado = formulario.cleaned_data['estado']            # Actualizar el estado y la columna de la tarjeta
            if tarjeta:
                # Llamada a la función actualizar_estado
                actualizar_estado(request, tarjeta.id, nuevo_estado.descripcion)
            
            if estado_anterior != nuevo_estado:
                contenido.agregar_historial(f"Cambio de estado '{estado_anterior}' a estado '{nuevo_estado}'")


            return redirect('contenidos')
        else:
            print(formulario.errors) 
    else:
        formulario = EditarContenidosForm(instance=contenido)

    return render(request, 'contenidos/editar.html', {'formulario': formulario})



@permission_required('Contenidos.delete_contenidos', raise_exception=True)
def eliminar_contenido(request, pk):
    """
    Vista para eliminar un contenido. Solicita confirmación antes de proceder con la eliminación.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - pk: ID del contenido a eliminar.

    Retorna:
    - HttpResponse que redirige a la lista de contenidos después de la eliminación, o muestra la página 'contenidos/confirmar_eliminacion.html' para confirmar la acción.
    """
    contenido = get_object_or_404(Contenidos, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        messages.success(request, 'Contenido eliminado con éxito.')
        return redirect('contenidos')
    return render(request, 'contenidos/confirmar_eliminacion.html', {'contenido': contenido})


@permission_required('Contenidos.view_contenidos', raise_exception=True)
def visualizar_contenido(request, id):
    """
    Vista para visualizar un contenido. También permite añadir nuevos comentarios relacionados 
    con el contenido.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - id: ID del contenido a visualizar.

    Retorna:
    - HttpResponse con la página 'contenidos/visualizar.html' que muestra el contenido y los comentarios asociados.
    """
    contenido = get_object_or_404(Contenidos, id=id)
    historial = contenido.historial.split("\n")
    # Incrementar el contador de lecturas
    contenido.numero_lecturas += 1
    contenido.save()

    comentarios = contenido.comentarios.all()  # Recuperar los comentarios relacionados con el contenido

    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            comentario = comentario_form.save(commit=False)
            comentario.usuario = request.user  # Asignar el usuario autenticado
            comentario.contenido = contenido   # Relacionar el comentario con el contenido actual
            comentario.save()
            #Si se crea el comentario, se envia una notificación por correo al autor
            context = {
                    'titulo': contenido.titulo,
                }      
            html_template = 'contenidos/comentado.html'
            html_message = render_to_string(html_template, context)
            subject = 'Alguien comentó tu publicación'
            message=EmailMessage(subject, html_message, 'cmseq052024@gmail.com', [contenido.autor.email])
            message.content_subtype = 'html'
            message.send()


            return redirect('visualizar_contenido', id=contenido.id)
    else:
        comentario_form = ComentarioForm()

    return render(request, 'contenidos/visualizar.html', {
        'contenido': contenido,
        'comentarios': comentarios,
        'comentario_form': comentario_form,
        'historial': historial
    })


def cargar_subcategorias(request):
    """
    Carga las subcategorías correspondientes a una categoría específica. 
    Se utiliza en la vista de creación y edición de contenidos.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.

    Retorna:
    - JsonResponse con las subcategorías asociadas a la categoría seleccionada.
    """
    categoria_id = request.GET.get('categoria_id')

    # Verificar si categoria_id es válido
    if categoria_id and categoria_id.isdigit():
        subcategorias = Subcategoria.objects.filter(categoriaPadre_id=int(categoria_id)).all()
    else:
        subcategorias = []  # Si no hay una categoría válida, devolver una lista vacía.

    return JsonResponse(list(subcategorias.values('id', 'nombre')), safe=False)


def eliminar_comentario(request, comentario_id):
    """
    Vista para eliminar un comentario. Solo el propietario del comentario o un usuario con permisos 
    adecuados puede eliminarlo. Solicita confirmación antes de proceder con la eliminación.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - comentario_id: ID del comentario a eliminar.

    Retorna:
    - HttpResponse que redirige a la página anterior o muestra la página de confirmación de eliminación.
    """
    comentario = get_object_or_404(Comentario, id=comentario_id)
    contenido = comentario.contenido
    print(f"Comentario encontrado: {comentario}")  # Para asegurarse de que el comentario está siendo encontrado correctamente

    if request.method == 'POST':
        if request.user == comentario.usuario or request.user.has_perm('Contenidos.delete_comentario'):
            comentario.delete()
            messages.success(request, 'Comentario eliminado con éxito.')
            return redirect('visualizar_contenido', id=contenido.id)

    return render(request, 'contenidos/confirmar_eliminacion_comentario.html', {'comentario': comentario})

def visualizar_contenido_borrador(request, id):
    """
    Vista para visualizar un contenido en borrador.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - id: ID del contenido a visualizar.

    Retorna:
    - HttpResponse con la página 'contenidos/visualizar.html' que muestra el contenido y los comentarios asociados.
    """
    contenido = get_object_or_404(Contenidos, id=id)

    return render(request, 'contenidos/borrador.html', {
        'contenido': contenido,
    })

def visualizar_contenido_revision(request, id):
    """
    Vista para visualizar un contenido en revisión.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - id: ID del contenido a visualizar.

    Retorna:
    - HttpResponse con la página 'contenidos/visualizar.html' que muestra el contenido y los comentarios asociados.
    """
    contenido = get_object_or_404(Contenidos, id=id)

    return render(request, 'contenidos/revision.html', {
        'contenido': contenido,
    })

def visualizar_contenido_aceptado(request, id):
    """
    Vista para visualizar un contenido en revisión.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - id: ID del contenido a visualizar.

    Retorna:
    - HttpResponse con la página 'contenidos/visualizar.html' que muestra el contenido y los comentarios asociados.
    """
    contenido = get_object_or_404(Contenidos, id=id)

    return render(request, 'contenidos/aceptado_rev.html', {
        'contenido': contenido,
})

def enviar_a_revision(request, id):
    """
    Vista para enviar un contenido a revisión.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - id: ID del contenido a enviar a revisión.

    Retorna:
    - HttpResponse que redirige a la página anterior o muestra la página de contenidos.

    Esta accion es agregada al historial del contenido como parte de un cambio de estado.
    """
    # Obtener el contenido con el ID proporcionado
    contenido = get_object_or_404(Contenidos, id=id)
    estado_anterior= contenido.estado
    tarjeta = Tarjeta.objects.filter(contenido=contenido).first()
    contenido.estado = get_object_or_404(Estado, id=4)  # Asumiendo que el ID 4 corresponde al estado "revisión"
    contenido.save()  # Guardar los cambios en la base de datos
    nuevo_estado = contenido.estado
    # Actualizar el estado de la tarjeta si existe
    
    tarjeta = Tarjeta.objects.filter(contenido=contenido).first()
    tarjeta.estado = nuevo_estado
    tarjeta.save()
    
    context = {
                    'titulo': contenido.titulo,
                }      
    html_template = 'contenidos/en_revision.html'
    html_message = render_to_string(html_template, context)
    subject = 'Cambio de estado de publicación'
    message=EmailMessage(subject, html_message, 'cmseq052024@gmail.com', [contenido.autor.email])
    message.content_subtype = 'html'
    message.send()
    if estado_anterior != nuevo_estado:
        contenido.agregar_historial(f"Cambio de estado '{estado_anterior}' a estado '{nuevo_estado}'")
        
    contenido.agregar_historial("Cambio de estado", "El contenido fue enviado a revision.")

    # Redirigir o devolver una respuesta
    return redirect('contenidos')  # Cambia a la vista a la que quieras redirigir

def aceptar_rechazar_contenido(request, id):
    """
    Vista para enviar un contenido a aceptado.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - id: ID del contenido a formatear.

    Retorna:
    - HttpResponse que redirige a la página anterior o muestra la página de contenidos.

    Esta accion es agregada al historial del contenido como parte de un cambio de estado.
    """
    # Obtener el contenido con el ID proporcionado
    contenido = get_object_or_404(Contenidos, id=id)
    tarjeta = Tarjeta.objects.filter(contenido=contenido).first() 
    # Cambiar el estado del contenido de 3 a 4
    if request.method == 'POST':
        accion = request.POST.get('accion')
        # Cambiar el estado del contenido
        if(accion == '0'): #accion 0 es rechazado
            contenido.estado = get_object_or_404(Estado, id=3)
            contenido.fecha_de_rechazados = datetime.now()
            context = {
                    'titulo': contenido.titulo,
                }      
            html_template = 'contenidos/rechazado.html'
            html_message = render_to_string(html_template, context)
            subject = 'Cambio de estado de publicación'
            message=EmailMessage(subject, html_message, 'cmseq052024@gmail.com', [contenido.autor.email])
            message.content_subtype = 'html'
            message.send()

            context = {
                    'titulo': contenido.titulo,
                }      
            html_template = 'contenidos/borrador_editor.html'
            html_message = render_to_string(html_template, context)
            subject = 'Cambio de estado de publicación'
            message=EmailMessage(subject, html_message, 'cmseq052024@gmail.com', [contenido.autor.email])
            message.content_subtype = 'html'
            message.send()
            contenido.agregar_historial("Cambio de estado", "El contenido ha sido rechazado.")
            contenido.agregar_historial("Cambio de estado", "El contenido ha sido enviado a borrador.")


        else: # esto es para aceptado
            contenido.estado = get_object_or_404(Estado, id=5)
            context = {
                    'titulo': contenido.titulo,
                }      
            html_template = 'contenidos/aceptado.html'
            html_message = render_to_string(html_template, context)
            subject = 'Cambio de estado de publicación'
            message=EmailMessage(subject, html_message, 'cmseq052024@gmail.com', [contenido.autor.email])
            message.content_subtype = 'html'
            message.send()
            contenido.agregar_historial("Cambio de estado", "El contenido ha sido aceptado.")

        contenido.save()  # Guardar los cambios en la base de datos
        nuevo_estado = contenido.estado
    # Actualizar el estado de la tarjeta si existe
    tarjeta = Tarjeta.objects.filter(contenido=contenido).first()
    tarjeta.estado = nuevo_estado
    tarjeta.save()
    # Redirigir o devolver una respuesta
    return redirect('contenidos')  # Cambia a la vista a la que quieras redirigir

def publicar_contenido(request, id):
    """
    Vista para enviar un contenido a activo.

    Parámetros:
    - request: HttpRequest object con la información de la solicitud.
    - id: ID del contenido a formatear.

    Retorna:
    - HttpResponse que redirige a la página anterior o muestra la página de contenidos.

    Esta accion es agregada al historial del contenido como parte de un cambio de estado.
    """
    # Obtener el contenido con el ID proporcionado
    contenido = get_object_or_404(Contenidos, id=id)
    tarjeta = Tarjeta.objects.filter(contenido=contenido).first() 
    # Cambiar el estado del contenido de 3 a 4
    if request.method == 'POST':
        accion = request.POST.get('accion')
        # Cambiar el estado del contenido
        if(accion == '0'): #rechazar es decir envia a en revision
            contenido.estado = get_object_or_404(Estado, id=4)
            contenido.fecha_de_rechazados = datetime.now()
            contenido.agregar_historial("Cambio de estado", "El contenido ha sido rechazado.")
            contenido.agregar_historial("Cambio de estado", "El contenido ha sido enviado a revision.")
        else: #el contenido se publica y se va al estado de activo
            contenido.estado = get_object_or_404(Estado, id=1)
            contenido.fecha_publicacion= datetime.now()
            context = {
                    'titulo': contenido.titulo,
                }      
            html_template = 'contenidos/publicado.html'
            html_message = render_to_string(html_template, context)
            subject = 'Cambio de estado de publicación'
            message=EmailMessage(subject, html_message, 'cmseq052024@gmail.com', [contenido.autor.email])
            message.content_subtype = 'html'
            message.send()
            contenido.agregar_historial("Cambio de estado", "El contenido se encuentra activo.")

        contenido.save()  # Guardar los cambios en la base de datos
        nuevo_estado = contenido.estado
    # Actualizar el estado de la tarjeta si existe
    if tarjeta:
        actualizar_estado(request, tarjeta.id, nuevo_estado.descripcion)
    # Redirigir o devolver una respuesta
    return redirect('contenidos')  # Cambia a la vista a la que quieras redirigir

def ver_historial(request, id):
    """
    Vista que permite visualizar el historial de un contenido especifico
    """
    contenido = get_object_or_404(Contenidos, id=id)
    return render(request, 'contenidos/historial.html', {'contenido': contenido})
