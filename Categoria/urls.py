from django.urls import path
from Categoria import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    #Categorias
    path('categorias', views.categorias, name='categorias'),
    path('categorias/crear', views.crear_cat, name='crear_cat'),
    path('categorias/editar', views.editar_cat, name='editar_cat'),
    #Subcategorias
    path('subcategorias', views.subcategorias, name='subcategorias'),
    path('subcategorias/crear', views.crear_sub, name='crear_sub'),
    path('subcategorias/editar', views.editar_sub, name='editar_sub')

]