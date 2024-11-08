from django.shortcuts import render
from .models import Contenidos
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime, timedelta

def reporte_contenidos_mas_leidos(request):
    # Inicializar variables para gráficos y otros datos
    graph_json1, graph_json2, graph_json3, graph_json4 = None, None, None, None
    tiempos_revision, contenidos_tiempos = [], []
    promedio_tiempo = "No hay contenidos disponibles para calcular el promedio."
    total_tiempo_revision, total_contenidos = 0, 0

    # Obtener las fechas del formulario
    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)

        # Gráfico 1: Top 10 Contenidos Más Leídos
        top_contenidos = Contenidos.objects.filter(
            fecha_publicacion__range=(fecha_inicio, fecha_fin)
        ).order_by('-numero_lecturas')[:10]
        nombres = [contenido.titulo for contenido in top_contenidos]
        lecturas = [contenido.numero_lecturas for contenido in top_contenidos]
        fig1 = go.Figure(data=[go.Bar(x=nombres, y=lecturas, name="Contenidos más leídos")])
        fig1.update_layout(title="Top 10 Contenidos Más Leídos", xaxis_title="Contenido", yaxis_title="Número de Lecturas")
        graph_json1 = plot(fig1, output_type='div')

        # Gráfico 2: Contenidos Publicados y Rechazados
        publicados = Contenidos.objects.filter(estado_id=1, fecha_publicacion__range=(fecha_inicio, fecha_fin)).count()
        rechazados = Contenidos.objects.filter(estado_id=3, fecha_de_rechazados__range=(fecha_inicio, fecha_fin)).count()
        fig2 = go.Figure(data=[
            go.Bar(x=['Contenidos'], y=[publicados], name='Publicados', marker_color='crimson'),
            go.Bar(x=['Contenidos'], y=[rechazados], name='Rechazados', marker_color='lightslategrey')
        ])
        fig2.update_layout(title="Contenidos Publicados y Rechazados", barmode='stack')
        graph_json2 = plot(fig2, output_type='div')

        # Gráfico 3: Promedio de Tiempo de Revisión por Contenido
        contenidos = Contenidos.objects.filter(
            fecha_creacion__range=(fecha_inicio, fecha_fin),
            fecha_publicacion__isnull=False
        )
        if contenidos.exists():
            for contenido in contenidos:
                tiempo_revision = contenido.fecha_publicacion - contenido.fecha_creacion
                total_tiempo_revision += tiempo_revision.total_seconds()
                total_contenidos += 1
                tiempos_revision.append(tiempo_revision)
                contenidos_tiempos.append((contenido, str(tiempo_revision)))

            promedio_segundos = total_tiempo_revision / total_contenidos
            promedio_tiempo = f"{int(promedio_segundos // 3600)}h {int((promedio_segundos % 3600) // 60)}m {int(promedio_segundos % 60)}s"
        
        fechas = [contenido.fecha_publicacion.strftime('%Y-%m-%d') for contenido in contenidos]
        cantidades = [1] * len(contenidos)
        fig3 = go.Figure(data=[go.Scatter(x=fechas, y=cantidades, mode='lines+markers')])
        fig3.update_layout(title="Promedio de Tiempo de Revisión por Contenido")
        graph_json3 = plot(fig3, output_type='div')

        # Gráfico 4: Contenidos Activos e Inactivos
        activos = Contenidos.objects.filter(estado_id=1, fecha_publicacion__range=(fecha_inicio, fecha_fin)).count()
        inactivos = Contenidos.objects.filter(estado_id=2, fecha_de_inactivacion__range=(fecha_inicio, fecha_fin)).count()
        fig4 = go.Figure(data=[
            go.Bar(x=['Estado'], y=[activos], name='Activos', marker_color='#0099ff'),
            go.Bar(x=['Estado'], y=[inactivos], name='Inactivos', marker_color='#404040')
        ])
        fig4.update_layout(title="Contenidos Activos e Inactivos", barmode='stack')
        graph_json4 = plot(fig4, output_type='div')

    # Enviar todos los gráficos y datos al contexto de la plantilla
    context = {
        'graph_json1': graph_json1,
        'graph_json2': graph_json2,
        'graph_json3': graph_json3,
        'graph_json4': graph_json4,
        'promedio_tiempo': promedio_tiempo,
        'contenidos_tiempos': contenidos_tiempos,
    }
    return render(request, 'reporte_contenidos_mas_leidos.html', context)
