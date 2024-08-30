from django.urls import path
from . import views

urlpatterns = [
    path('', views.plantillas, name='plantillas'),
    path('crear', views.crear, name='crear'),
    path('editar', views.editar, name='editar')
]