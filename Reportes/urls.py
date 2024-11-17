from django.urls import path
from . import views

urlpatterns = [
    path('reporte_todos/', views.reporte_todos, name='reporte_todos'),
    
]