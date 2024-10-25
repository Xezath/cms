from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from .models import Tablero, Tarjeta, Columna
from Contenidos.models import Estado
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@login_required
@permission_required('TableroKanban.ver_propio_tablero', raise_exception=True)
def tablero_kanban(request, tablero_id):
    """
    Vista para visualizar un tablero Kanban específico, sus columnas y tarjetas,
    con acceso y visualización filtrados según el rol y permisos del usuario.

    Args:
        request (HttpRequest): Objeto HttpRequest que contiene datos de la solicitud.
        tablero_id (int): ID del tablero a visualizar.

    Returns:
        HttpResponse: Renderiza la plantilla 'TableroKanban/tablero.html' con el contexto
        del tablero, las tarjetas organizadas por estado y la autorización para cambiar estados.

    Raises:
        PermissionDenied: Si el usuario no tiene permisos para ver el tablero especificado.
    """
    tablero = get_object_or_404(Tablero, id=tablero_id)
    columnas = tablero.columnas.prefetch_related('tarjetas').all()

    tarjetas_por_estado = {
        'Activas': [],
        'Inactivas': [],
        'Borrador': [],
        'Revision': [],
        'Aceptadas': []
    }

    for columna in columnas:
        # Permitir a los roles Administrador, Publicador y Editor ver las tarjetas en revisión de todos
        if request.user.groups.filter(name__in=['Administrador', 'Publicador']).exists():
            tarjetas = columna.tarjetas.all()
        elif request.user.groups.filter(name__in=['Editor']).exists() and columna.estado.descripcion == 'Revision':
            tarjetas = columna.tarjetas.all()
        else:
            tarjetas = columna.tarjetas.filter(autor=request.user)

        for tarjeta in tarjetas:
            if tarjeta.columna.estado.descripcion == 'Activo':
                tarjetas_por_estado['Activas'].append(tarjeta)
            elif tarjeta.columna.estado.descripcion == 'Inactivo':
                tarjetas_por_estado['Inactivas'].append(tarjeta)
            elif tarjeta.columna.estado.descripcion == 'Borrador':
                tarjetas_por_estado['Borrador'].append(tarjeta)
            elif tarjeta.columna.estado.descripcion == 'Revision':
                tarjetas_por_estado['Revision'].append(tarjeta)
            elif tarjeta.columna.estado.descripcion == 'Aceptado':
                tarjetas_por_estado['Aceptadas'].append(tarjeta)

    puede_cambiar_estado = request.user.has_perm('TableroKanban.cambiar_estado_tarjeta')

    return render(request, 'TableroKanban/tablero.html', {
        'tablero': tablero,
        'tarjetas_por_estado': tarjetas_por_estado,
        'puede_cambiar_estado': puede_cambiar_estado
    })


@csrf_exempt
@permission_required('TableroKanban.cambiar_estado_tarjeta', raise_exception=True)
def actualizar_estado(request, tarjeta_id, nuevo_estado):
    """
    Vista que actualiza el estado de una tarjeta.

    Args:
        request: El objeto de la solicitud HTTP.
        tarjeta_id (int): El ID de la tarjeta a actualizar.
        nuevo_estado (str): El nuevo estado que se le quiere asignar a la tarjeta.

    Returns:
        JsonResponse: Respuesta en formato JSON indicando el resultado de la operación.
    """
    if request.method == 'POST':
        try:
            # Buscar la tarjeta por su ID
            tarjeta = Tarjeta.objects.get(id=tarjeta_id)
            
            # Buscar el estado correspondiente al nuevo estado
            estado = Estado.objects.get(descripcion=nuevo_estado)  
            
            # Buscar la columna correspondiente a ese estado en el mismo tablero
            columna = Columna.objects.get(estado=estado, tablero=tarjeta.columna.tablero)
            
            # Actualizar la tarjeta con la nueva columna (basada en el estado)
            tarjeta.columna = columna
            tarjeta.estado = estado
            tarjeta.save()

            # Sincronizar el estado del contenido relacionado
            if hasattr(tarjeta, 'contenido'):
                contenido = tarjeta.contenido  # Obtiene el contenido relacionado
                contenido.estado = estado  # Cambia el estado del contenido
                contenido.save()  # Guarda los cambios
            
            return JsonResponse({'status': 'ok'})
        except Tarjeta.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Tarjeta no encontrada'}, status=404)
        except Estado.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Estado no encontrado'}, status=404)
        except Columna.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Columna no encontrada para el estado especificado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)  # Manejo de errores genéricos
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

