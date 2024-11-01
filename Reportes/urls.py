from django.urls import path
from . import views

urlpatterns = [
    path('contenidos_mas_leidos/', views.reporte_contenidos_mas_leidos, name='reporte_contenidos_mas_leidos'),
]
