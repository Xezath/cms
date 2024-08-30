from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('categorias', views.categorias, name='categorias'),
    path('categorias/crear', views.crear, name='crear'),
    path('categorias/editar', views.editar, name='editar'),
    #Subcategorias
    path('subcategorias', views.subcategorias, name='subcategorias'),
    path('subcategorias/crear', views.crear_sub, name='crear_sub'),
    path('subcategorias/editar', views.editar_sub, name='editar_sub')
]