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

def reporte_contenidos_mas_leidos(request):
    # Obtener los 10 artículos más leídos
    top_contenidos = Contenidos.objects.order_by('-numero_lecturas')[:10]
    
    # Extraer los datos de los artículos para graficar
    nombres = [contenido.titulo for contenido in top_contenidos]
    lecturas = [contenido.numero_lecturas for contenido in top_contenidos]

    # Crear el gráfico usando Plotly
    fig = px.bar(
        x=nombres,
        y=lecturas,
        title="Top 10 Contenidos Más Leídos",
        labels={'x': "Contenido", 'y': "Número de Lecturas"}
    )
    
    # Convertir el gráfico a JSON para enviar al template
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render(request, 'reporte_contenidos_mas_leidos.html', {'graph_json': graph_json})


def reporte_contenidos_publicados_rechazados(request):
    graph_json = None  # Inicializamos el gráfico vacío por defecto
    
    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')

        # Convertir fechas a objetos datetime
        fecha_inicio = timezone.datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = timezone.datetime.strptime(fecha_fin_str, '%Y-%m-%d')

        # Filtrar contenidos según el rango de fechas
        contenidos_publicados = Contenidos.objects.filter(estado_id=1, fecha_publicacion__range=(fecha_inicio, fecha_fin)).count()
        contenidos_rechazados = Contenidos.objects.filter(estado_id=3, fecha_de_rechazados__range=(fecha_inicio, fecha_fin)).count()

        # Imprimir valores para depuración
        print(f"Fecha Inicio: {fecha_inicio}, Fecha Fin: {fecha_fin}")
        print(f"Contenidos Publicados: {contenidos_publicados}")
        print(f"Contenidos Rechazados: {contenidos_rechazados}")
        
        # Crear los datos del gráfico de líneas
        fechas = ['Publicados', 'Rechazados']  # Etiquetas para el eje X
        cantidades = [contenidos_publicados, contenidos_rechazados]  # Cantidades para el eje Y

        # Crear el gráfico de líneas
        trace = go.Scatter(x=fechas, y=cantidades, mode='lines+markers', name='Contenidos')
        layout = go.Layout(title='Contenidos Publicados y Rechazados', xaxis=dict(title='Estado'), yaxis=dict(title='Cantidad'))
        fig = go.Figure(data=[trace], layout=layout)

        # Convertir el gráfico a JSON para pasarlo a la plantilla
        graph_json = plot(fig, output_type='div')

    return render(request, 'reporte_contenidos_publicados_rechazados.html', {'graph_json': graph_json})