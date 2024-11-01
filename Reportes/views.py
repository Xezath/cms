from django.shortcuts import render
from .models import Contenidos
import plotly.express as px
import plotly
import json


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

