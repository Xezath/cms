from django.urls import path
from . import views

urlpatterns = [
    
    path('contenidos_mas_leidos/', views.reporte_contenidos_mas_leidos, name='reporte_contenidos_mas_leidos'),
    path('contenidos_publicados_rechazados/', views.reporte_contenidos_publicados_rechazados, name='reporte_contenidos_publicados_rechazados'),
    path('reporte-promedio-tiempo-revision/', views.reporte_promedio_tiempo_revision, name='reporte_promedio_tiempo_revision'),
]
