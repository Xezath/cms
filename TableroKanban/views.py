from django.shortcuts import render, get_object_or_404
from .models import Tablero, Tarjeta

def tablero_kanban(request, tablero_id):  # Aceptar tablero_id como argumento
    tablero = get_object_or_404(Tablero, id=tablero_id)  # Obtener el tablero por ID
    columnas = tablero.columnas.prefetch_related('tarjetas').all()

    # Crear un diccionario para almacenar tarjetas por estado
    tarjetas_por_estado = {
        'Activas': [],
        'Inactivas': [],
        'Borrador': []
    }

    # Llenar el diccionario con tarjetas de cada columna
    for columna in columnas:
        for tarjeta in columna.tarjetas.all():
            if tarjeta.columna.estado.descripcion == 'Activo':
                tarjetas_por_estado['Activas'].append(tarjeta)
            elif tarjeta.columna.estado.descripcion == 'Inactivo':
                tarjetas_por_estado['Inactivas'].append(tarjeta)
            elif tarjeta.columna.estado.descripcion == 'Borrador':
                tarjetas_por_estado['Borrador'].append(tarjeta)

    return render(request, 'TableroKanban/tablero.html', {
        'tablero': tablero,
        'tarjetas_por_estado': tarjetas_por_estado
    })
