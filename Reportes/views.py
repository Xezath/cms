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
def generar_reporte_contenidos_mas_leidos(fecha_inicio, fecha_fin):
    """
    Genera un reporte de los contenidos más leídos dentro de la página en un rango de fechas especificado.
    Presenta un gráfico de barras con los contenidos más leídos entre las fechas seleccionadas.
    """
    top_contenidos = Contenidos.objects.filter(
        fecha_publicacion__range=(fecha_inicio, fecha_fin)
    ).order_by('-numero_lecturas')[:10]

    nombres = [contenido.titulo for contenido in top_contenidos]
    lecturas = [contenido.numero_lecturas for contenido in top_contenidos]

    trace = go.Bar(x=nombres, y=lecturas, name="Contenidos más leídos")
    layout = go.Layout(
        title=f"Top 10 Contenidos Más Leídos entre {fecha_inicio.date()} y {fecha_fin.date()}",
        xaxis=dict(title='Contenido'),
        yaxis=dict(title='Número de Lecturas')
    )
    fig = go.Figure(data=[trace], layout=layout)
    return plot(fig, output_type='div')


def generar_reporte_contenidos_publicados_rechazados(fecha_inicio, fecha_fin):
    """
    Genera un reporte de contenidos publicados y rechazados en un rango de fechas.
    Muestra un gráfico de barras apiladas para visualizar la cantidad de contenidos en ambos estados.
    """
    contenidos_publicados = Contenidos.objects.filter(estado_id=1, fecha_publicacion__range=(fecha_inicio, fecha_fin)).count()
    contenidos_rechazados = Contenidos.objects.filter(estado_id=3, fecha_de_rechazados__range=(fecha_inicio, fecha_fin)).count()

    trace_publicados = go.Bar(x=['Contenidos'], y=[contenidos_publicados], name='Publicados', marker_color='crimson')
    trace_rechazados = go.Bar(x=['Contenidos'], y=[contenidos_rechazados], name='Rechazados', marker_color='lightslategrey')
    layout = go.Layout(
        title='Contenidos Publicados y Rechazados',
        xaxis=dict(title='Estado'),
        yaxis=dict(title='Cantidad'),
        barmode='stack'
    )
    fig = go.Figure(data=[trace_publicados, trace_rechazados], layout=layout)
    return plot(fig, output_type='div')


def generar_reporte_promedio_tiempo_revision(fecha_inicio, fecha_fin):
    """
    Calcula el promedio de tiempo de revisión entre la creación y la publicación de contenidos en un rango de fechas.
    Muestra un gráfico de líneas con la cantidad de contenidos revisados y un resumen del tiempo promedio.
    """
    tiempos_revision = []  # Lista para almacenar los tiempos de revisión formateados
    contenidos_tiempos = []  # Lista para almacenar los contenidos con tiempos de revisión formateados
    total_tiempo_revision = 0  # Variable para acumular el total de tiempo de revisión
    total_contenidos = 0  # Variable para contar el número total de contenidos
    promedio_tiempo = "No hay contenidos disponibles para calcular el promedio."  # Valor predeterminado

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
    
    else:
        # Crear un gráfico vacío para manejar el caso de que no haya datos
        layout = go.Layout(title='No hay datos para el rango de fechas seleccionado', xaxis=dict(title='Fecha'), yaxis=dict(title='Promedio de Tiempo de Revisión'))
        fig = go.Figure(layout=layout)
    return {'grafico': plot(fig, output_type='div'), 'promedio_tiempo': promedio_tiempo, 'contenidos_tiempos': contenidos_tiempos}


def generar_reporte_contenidos_inactivos(fecha_inicio, fecha_fin):
    """
    Genera un reporte de contenidos inactivos en un rango de fechas, mostrando una comparación con los contenidos activos.
    Muestra un gráfico de barras con la cantidad de contenidos activos e inactivos.
    """
    contenidos_activos = Contenidos.objects.filter(
        estado_id=1, fecha_publicacion__range=(fecha_inicio, fecha_fin)
    ).count()
    contenidos_inactivos = Contenidos.objects.filter(
        estado_id=2, fecha_de_inactivacion__range=(fecha_inicio, fecha_fin)
    ).count()

    trace_activos = go.Bar(x=['Contenidos'], y=[contenidos_activos], name='Activos', marker_color='blue')
    trace_inactivos = go.Bar(x=['Contenidos'], y=[contenidos_inactivos], name='Inactivos', marker_color='grey')
    layout = go.Layout(
        title='Contenidos Activos e Inactivos',
        xaxis=dict(title='Estado'),
        yaxis=dict(title='Cantidad')
    )
    fig = go.Figure(data=[trace_activos, trace_inactivos], layout=layout)
    return plot(fig, output_type='div')


def reporte_todos(request):
    graph_contenidos_mas_leidos = ""
    graph_contenidos_publicados_rechazados = ""
    graph_promedio_tiempo_revision = ""
    graph_contenidos_inactivos = ""

    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)

        graph_contenidos_mas_leidos = generar_reporte_contenidos_mas_leidos(fecha_inicio, fecha_fin)
        graph_contenidos_publicados_rechazados = generar_reporte_contenidos_publicados_rechazados(fecha_inicio, fecha_fin)
        graph_promedio_tiempo_revision = generar_reporte_promedio_tiempo_revision(fecha_inicio, fecha_fin)
        graph_contenidos_inactivos = generar_reporte_contenidos_inactivos(fecha_inicio, fecha_fin)

    return render(request, 'reporte_todos.html', {
        'graph_contenidos_mas_leidos': graph_contenidos_mas_leidos,
        'graph_contenidos_publicados_rechazados': graph_contenidos_publicados_rechazados,
        'graph_promedio_tiempo_revision': graph_promedio_tiempo_revision,
        'graph_contenidos_inactivos': graph_contenidos_inactivos,
    })
