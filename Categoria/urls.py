from django.urls import path
from Categoria import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    #Categorias
    path('categorias', views.categorias, name='categorias'),
    path('categorias/crear', views.crear_cat, name='crear_cat'),
    path('borrar_cat/<int:id>', views.borrar_cat, name='borrar_cat'),
    path('categorias/editar/<int:id>', views.editar_cat, name='editar_cat'),
    path('mensajeExito', views.mensajeExito, name='mensajeExito'),
    #Subcategorias
    path('subcategorias', views.subcategorias, name='subcategorias'),
    path('subcategorias/crear', views.crear_sub, name='crear_sub'),
    path('borrar_sub/<int:id>', views.borrar_sub, name='borrar_sub'),
    path('subcategorias/editar/<int:id>', views.editar_sub, name='editar_sub'),
    path('mensajeExito_sub', views.mensajeExito_sub, name='mensajeExito_sub')

]