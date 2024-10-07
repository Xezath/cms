from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from .models import Tablero

@login_required
@permission_required('TableroKanban.ver_propio_tablero', raise_exception=True)
def tablero_kanban(request, tablero_id):
    tablero = get_object_or_404(Tablero, id=tablero_id)
    columnas = tablero.columnas.prefetch_related('tarjetas').all()

    # Crear un diccionario para almacenar tarjetas por estado
    tarjetas_por_estado = {
        'Activas': [],
        'Inactivas': [],
        'Borrador': []
    }

    # Llenar el diccionario con tarjetas de cada columna
    for columna in columnas:
        if request.user.groups.filter(name='Administrador').exists():
            # Si el usuario es administrador, muestra todas las tarjetas
            tarjetas = columna.tarjetas.all()
        else:
            # Si el usuario no es administrador, solo muestra sus tarjetas
            tarjetas = columna.tarjetas.filter(autor=request.user)

        for tarjeta in tarjetas:
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
