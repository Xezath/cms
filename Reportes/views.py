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

def reporte_contenidos_mas_leidos(request):
    graph_json = None  # Inicializamos el gráfico vacío por defecto
    
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
    graph_json = None  # Inicializamos el gráfico vacío por defecto
    
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
    graph_json = None  # Inicializamos el gráfico vacío por defecto
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
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')+ timedelta(days=1) - timedelta(seconds=1)

        # Filtrar contenidos según el rango de fechas
        contenidos = Contenidos.objects.filter(
            fecha_creacion__range=(fecha_inicio, fecha_fin), 
            fecha_publicacion__isnull=False
        )
        
        # Si hay contenidos, calcular los tiempos de revisión y el promedio
        if contenidos.exists():
            # Calcular el tiempo de revisión en horas, minutos y segundos
            for contenido in contenidos:
                if contenido.fecha_creacion and contenido.fecha_publicacion:
                    tiempo_revision = contenido.fecha_publicacion - contenido.fecha_creacion
                    total_tiempo_revision += tiempo_revision.seconds  # Acumulamos el tiempo total
                    total_contenidos += 1  # Contamos los contenidos

                    horas = tiempo_revision.seconds // 3600
                    minutos = (tiempo_revision.seconds % 3600) // 60
                    segundos = tiempo_revision.seconds % 60
                    tiempo_formateado = f"{horas}h {minutos}m {segundos}s"
                    tiempos_revision.append(tiempo_formateado)
                    contenidos_tiempos.append((contenido, tiempo_formateado))

            # Calcular el promedio de tiempo de revisión (si hay contenidos)
            promedio_segundos = total_tiempo_revision / total_contenidos
            promedio_horas = int(promedio_segundos // 3600)
            promedio_minutos = int((promedio_segundos % 3600) // 60)
            promedio_segundos = int(promedio_segundos % 60)
            promedio_tiempo = f"{promedio_horas}h {promedio_minutos}m {promedio_segundos}s"
        
        # Crear los datos del gráfico de líneas (para mostrar la cantidad de contenidos por fecha de publicación)
        fechas = [contenido.fecha_publicacion.strftime('%Y-%m-%d %H:%M:%S') for contenido in contenidos]  # Fechas de publicación
        cantidades = [1 for _ in contenidos]  # Solo contar 1 por cada contenido

        # Crear el gráfico de líneas
        trace = go.Scatter(x=fechas, y=cantidades, mode='lines+markers', name='Contenidos')
        layout = go.Layout(title='Promedio de Tiempo de Revisión por Contenido', xaxis=dict(title='Fecha de Publicación'), yaxis=dict(title='Cantidad de Contenidos'))
        fig = go.Figure(data=[trace], layout=layout)

        # Convertir el gráfico a JSON para pasarlo a la plantilla
        graph_json = plot(fig, output_type='div')

    return render(request, 'reporte_promedio_tiempo_revision.html', {
        'graph_json': graph_json, 
        'contenidos_tiempos': contenidos_tiempos,
        'promedio_tiempo': promedio_tiempo
    })