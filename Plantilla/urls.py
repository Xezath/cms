from django.urls import path
from . import views

urlpatterns = [
    path('', views.plantillas, name='plantillas'),
    path('crear_plantilla', views.crear_plantilla, name='crear_plantilla'),
    path('editar_plantilla/<int:id>', views.editar_plantilla, name='editar_plantilla'),
    path('borrar_plantilla/<int:id>', views.borrar_plantilla, name='borrar_plantilla'),
    path('mensajeExito_plantilla', views.mensajeExito_plantilla, name='mensajeExito_plantilla')
]