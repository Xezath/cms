from django.shortcuts import redirect, render, get_object_or_404
from .models import Tablero, Tarjeta

def tablero_kanban(request, tablero_id):
    tablero = get_object_or_404(Tablero, id=tablero_id)

    # Filtrar las tarjetas a través de la relación con la columna que está relacionada con el tablero
    tarjetas_activas = Tarjeta.objects.filter(columna__tablero=tablero, estado='activo')
    tarjetas_inactivas = Tarjeta.objects.filter(columna__tablero=tablero, estado='inactivo')
    tarjetas_borrador = Tarjeta.objects.filter(columna__tablero=tablero, estado='borrador')

    # Crear un diccionario para agrupar las tarjetas por estado
    tarjetas_por_estado = {
        'Activas': tarjetas_activas,
        'Inactivas': tarjetas_inactivas,
        'Borrador': tarjetas_borrador,
    }

    return render(request, 'TableroKanban/tablero.html', {'tablero': tablero, 'tarjetas_por_estado': tarjetas_por_estado})
