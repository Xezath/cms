from django.urls import path
from . import views

urlpatterns = [
    path('reportes/', views.reporte_principal, name='reporte_principal'),
    path('contenidos_mas_leidos/', views.reporte_contenidos_mas_leidos, name='reporte_contenidos_mas_leidos'),
    path('contenidos_publicados_rechazados/', views.reporte_contenidos_publicados_rechazados, name='reporte_contenidos_publicados_rechazados'),
    path('contenidos_inactivos/', views.reporte_contenidos_inactivos, name='reporte_contenidos_inactivos'),
    path('reporte-promedio-tiempo-revision/', views.reporte_promedio_tiempo_revision, name='reporte_promedio_tiempo_revision'),
    
]
