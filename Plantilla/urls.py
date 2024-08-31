from django.urls import path
from . import views

urlpatterns = [
    path('', views.plantillas, name='plantillas'),
    path('crear', views.crear_plantilla, name='crear'),
    path('editar', views.editar_plantilla, name='editar')
]