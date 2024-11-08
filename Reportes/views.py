from django.shortcuts import render, get_object_or_404
from .models import Contenidos, Estado
import plotly.express as px
import plotly
import json
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse
from plotly.offline import plot
import plotly.graph_objs as go
from datetime import datetime
from django.db.models import Avg, F, ExpressionWrapper, fields, DurationField
from datetime import timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from collections import defaultdict

def reporte_contenidos_mas_leidos(request):
    """
    Genera un reporte de los contenidos más leídos dentro de la página en un rango de fechas especificado.
    Presenta un gráfico de barras con los contenidos más leídos entre las fechas seleccionadas.
    
    Args:
        request: Objeto HttpRequest que contiene datos sobre la solicitud de usuario.
    
    Returns:
        HttpResponse: Renderiza la plantilla 'reporte_contenidos_mas_leidos.html' con el gráfico en formato JSON.
    """
    graph_json = ""
    
    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')

        # Convertir las fechas de cadena a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)

        # Filtrar los contenidos según el rango de fechas
        top_contenidos = Contenidos.objects.filter(
            fecha_publicacion__range=(fecha_inicio, fecha_fin)
        ).order_by('-numero_lecturas')[:10]

        # Extraer los datos de los artículos para graficar
        nombres = [contenido.titulo for contenido in top_contenidos]
        lecturas = [contenido.numero_lecturas for contenido in top_contenidos]

        # Crear el gráfico de barras con Plotly
        trace = go.Bar(
            x=nombres,
            y=lecturas,
            name="Contenidos más leídos"
        )
        layout = go.Layout(
            title=f"Top 10 Contenidos Más Leídos entre {fecha_inicio.date()} y {fecha_fin.date()}",
            xaxis=dict(title='Contenido'),
            yaxis=dict(title='Número de Lecturas')
        )
        fig = go.Figure(data=[trace], layout=layout)

        # Convertir el gráfico a JSON para pasarlo a la plantilla
        graph_json = fig.to_json()

    return render(request, 'reporte_contenidos_mas_leidos.html', {'graph_json': graph_json})


def reporte_contenidos_publicados_rechazados(request):
    """
    Genera un reporte de contenidos publicados y rechazados en un rango de fechas.
    Muestra un gráfico de barras apiladas para visualizar la cantidad de contenidos en ambos estados.

    Args:
        request: Objeto HttpRequest que contiene datos sobre la solicitud de usuario.

    Returns:
        HttpResponse: Renderiza la plantilla 'reporte_contenidos_publicados_rechazados.html' con el gráfico en formato JSON.
    """
    graph_json = ""

    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')

        # Convertir fechas a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')+ timedelta(days=1) - timedelta(seconds=1)

        # Filtrar contenidos según el rango de fechas
        contenidos_publicados = Contenidos.objects.filter(estado_id=1, fecha_publicacion__range=(fecha_inicio, fecha_fin)).count()
        contenidos_rechazados = Contenidos.objects.filter(estado_id=3, fecha_de_rechazados__range=(fecha_inicio, fecha_fin)).count()

        # Imprimir valores para depuración
        print(f"Fecha Inicio: {fecha_inicio}, Fecha Fin: {fecha_fin}")
        print(f"Contenidos Publicados: {contenidos_publicados}")
        print(f"Contenidos Rechazados: {contenidos_rechazados}")
        
        # Crear los datos del gráfico de barras apiladas
        fechas = ['Contenidos']  # Etiqueta para el eje X
        publicados = [contenidos_publicados]  # Cantidad de contenidos publicados
        rechazados = [contenidos_rechazados]  # Cantidad de contenidos rechazados

        # Crear el gráfico de barras apiladas con colores azul y rojo
        trace_publicados = go.Bar(
            x=fechas,
            y=publicados,
            name='Publicados',
            marker_color='crimson'  # Color crimson para 'Publicados'
        )
        trace_rechazados = go.Bar(
            x=fechas,
            y=rechazados,
            name='Rechazados',
            marker_color='lightslategrey'  # Color lightslategrey para 'Rechazados'
        )

        # Crear el layout con barmode='stack'
        layout = go.Layout(
            title='Contenidos Publicados y Rechazados',
            xaxis=dict(title='Estado'),
            yaxis=dict(title='Cantidad'),
            barmode='stack'  # Apilar las barras
        )

        # Crear la figura con los dos trazos (barras apiladas)
        fig = go.Figure(data=[trace_publicados, trace_rechazados], layout=layout)

        # Convertir el gráfico a JSON para pasarlo a la plantilla
        graph_json = plot(fig, output_type='div')

    return render(request, 'reporte_contenidos_publicados_rechazados.html', {'graph_json': graph_json})


def reporte_promedio_tiempo_revision(request):
    """
    Calcula el promedio de tiempo de revisión entre la creación y la publicación de contenidos en un rango de fechas.
    Muestra un gráfico de líneas con la cantidad de contenidos revisados y un resumen del tiempo promedio.

    Args:
        request: Objeto HttpRequest que contiene datos sobre la solicitud de usuario.

    Returns:
        HttpResponse: Renderiza la plantilla 'reporte_promedio_tiempo_revision.html' con el gráfico y los tiempos de revisión.
    """
    graph_json = ""
    tiempos_revision = []  # Lista para almacenar los tiempos de revisión formateados
    contenidos_tiempos = []  # Lista para almacenar los contenidos con tiempos de revisión formateados
    total_tiempo_revision = 0  # Variable para acumular el total de tiempo de revisión
    total_contenidos = 0  # Variable para contar el número total de contenidos
    promedio_tiempo = "No hay contenidos disponibles para calcular el promedio."  # Valor predeterminado

    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')

        # Convertir fechas a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)

        # Filtrar contenidos según el rango de fechas
        contenidos = Contenidos.objects.filter(
            fecha_creacion__range=(fecha_inicio, fecha_fin), 
            fecha_publicacion__isnull=False
        )

        # Si hay contenidos, calcular los tiempos de revisión y el promedio
        if contenidos.exists():
            # Crear un diccionario para almacenar los tiempos de revisión por día
            tiempos_por_dia = defaultdict(list)

            # Llenar el diccionario con los tiempos de revisión
            for contenido in contenidos:
                if contenido.fecha_creacion and contenido.fecha_publicacion:
                    tiempo_revision = contenido.fecha_publicacion - contenido.fecha_creacion
                    total_tiempo_revision += tiempo_revision.seconds  # Acumulamos el tiempo total en segundos
                    total_contenidos += 1  # Contamos los contenidos

                    # Calcular tiempo formateado para la tabla
                    horas = tiempo_revision.seconds // 3600
                    minutos = (tiempo_revision.seconds % 3600) // 60
                    segundos = tiempo_revision.seconds % 60
                    tiempo_formateado = f"{horas}h {minutos}m {segundos}s"
                    tiempos_revision.append(tiempo_formateado)
                    contenidos_tiempos.append((contenido, tiempo_formateado))

                    # Agregar el tiempo de revisión en segundos al día correspondiente
                    fecha_publicacion = contenido.fecha_publicacion
                    tiempos_por_dia[fecha_publicacion].append(tiempo_revision.seconds)

            # Calcular el promedio total de tiempo de revisión
            promedio_segundos = total_tiempo_revision / total_contenidos
            promedio_horas = int(promedio_segundos // 3600)
            promedio_minutos = int((promedio_segundos % 3600) // 60)
            promedio_segundos = int(promedio_segundos % 60)
            promedio_tiempo = f"{promedio_horas}h {promedio_minutos}m {promedio_segundos}s"

            # Preparar datos para el gráfico
            fechas = []
            promedios_diarios = []

            # Calcular el promedio diario de tiempo de revisión en formato hh:mm:ss
            for fecha, tiempos in tiempos_por_dia.items():
                promedio_dia_segundos = sum(tiempos) / len(tiempos)  # Promedio en segundos
                promedio_dia_horas = promedio_dia_segundos // 3600
                promedio_dia_minutos = (promedio_dia_segundos % 3600) // 60
                promedio_dia_segundos = promedio_dia_segundos % 60

                # Convertir promedio a formato hh:mm:ss
                promedio_dia_formateado = f"{int(promedio_dia_horas)}h {int(promedio_dia_minutos)}m {int(promedio_dia_segundos)}s"

                fechas.append(fecha)
                promedios_diarios.append(promedio_dia_formateado)  # Usar el formato hh:mm:ss

            # Crear el gráfico de promedio de tiempo de revisión
            trace = go.Scatter(x=promedios_diarios, y=fechas, mode='lines+markers', name='Promedio de Tiempo de Revisión')
            layout = go.Layout(title='Promedio Diario de Tiempo de Revisión', xaxis=dict(title='Promedio de Tiempo de Revisión'), yaxis=dict(title='Fecha de Publicación'))
            fig = go.Figure(data=[trace], layout=layout)

            # Convertir el gráfico a JSON para pasarlo a la plantilla
            graph_json = plot(fig, output_type='div')

    return render(request, 'reporte_promedio_tiempo_revision.html', {
        'graph_json': graph_json, 
        'contenidos_tiempos': contenidos_tiempos,
        'promedio_tiempo': promedio_tiempo
    })

def reporte_contenidos_inactivos(request):
    """
    Genera un reporte de contenidos inactivos en un rango de fechas, mostrando una comparación con los contenidos activos.
    Muestra un gráfico de barras con la cantidad de contenidos activos e inactivos.

    Args:
        request: Objeto HttpRequest que contiene datos sobre la solicitud de usuario.

    Returns:
        HttpResponse: Renderiza la plantilla 'reporte_contenidos_inactivos.html' con el gráfico de contenidos activos e inactivos.
    """
    graph_json = ""

    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')

        # Convertir las fechas de cadena a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')+ timedelta(days=1) - timedelta(seconds=1)

        # Filtrar los contenidos en el rango de fechas especificado
        contenidos_inactivos = Contenidos.objects.filter(
            estado_id=2,
            fecha_de_inactivacion__range=(fecha_inicio, fecha_fin)
        ).values('fecha_de_inactivacion')

        contenidos_activos = Contenidos.objects.filter(
            estado_id=1,
            fecha_publicacion__range=(fecha_inicio, fecha_fin)
        ).values('fecha_publicacion')

        # Crear listas de fechas y estados
        fechas_inactivos = [contenido['fecha_de_inactivacion'] for contenido in contenidos_inactivos]
        fechas_activos = [contenido['fecha_publicacion'] for contenido in contenidos_activos]

        # Crear un DataFrame para el gráfico
        data = {
            'Fecha': fechas_inactivos + fechas_activos,
            'Estado': ['Inactivo'] * len(fechas_inactivos) + ['Activo'] * len(fechas_activos)
        }

        # Crear la figura usando go.Figure y añadir la información como gráfico de barras
        import plotly.graph_objects as go
        import plotly.figure_factory as ff

        # Add table data
        table_data = [['']]

        # Initialize a figure with ff.create_table(table_data)
        fig = ff.create_table(table_data, height_constant=60)

        # Add graph data
        teams = ['Estado']
        GFPG = [contenidos_activos.count()]
        GAPG = [contenidos_inactivos.count()]

        # Make traces for graph
        trace1 = go.Bar(x=teams, y=GFPG, xaxis='x2', yaxis='y2',
                        marker=dict(color='#0099ff'),
                        name='Activos')
        trace2 = go.Bar(x=teams, y=GAPG, xaxis='x2', yaxis='y2',
                        marker=dict(color='#404040'),
                        name='Inactivos')

        # Add trace data to figure
        fig.add_traces([trace1, trace2])

        # initialize xaxis2 and yaxis2
        fig['layout']['xaxis2'] = {}
        fig['layout']['yaxis2'] = {}

        # Edit layout for subplots
        fig.layout.yaxis.update({'domain': [0, .45]})
        fig.layout.yaxis2.update({'domain': [.6, 1]})

        # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
        fig.layout.yaxis2.update({'anchor': 'x2'})
        fig.layout.xaxis2.update({'anchor': 'y2'})
        fig.layout.yaxis2.update({'title': 'Cantidad'})

        # Update the margins to add a title and see graph x-labels.
        fig.layout.margin.update({'t':75, 'l':50})
        fig.layout.update({'title': 'Contenidos activos e inactivos'})

        # Update the height because adding a graph vertically will interact with
        # the plot height calculated for the table
        fig.layout.update({'height':800})

        # Plot!
        graph_json = plot(fig, output_type='div')
    
    return render(request, 'reporte_contenidos_inactivos.html', {'graph_json': graph_json})

from django.shortcuts import render

def reporte_principal(request):
    return render(request, 'reporte_principal.html')
