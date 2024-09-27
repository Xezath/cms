from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import contenidos, crear_contenido, editar_contenido, eliminar_contenido, visualizar_contenido, cargar_subcategorias, eliminar_comentario

urlpatterns = [
    path('contenidos/', contenidos, name='contenidos'),
    path('contenidos/crear/', crear_contenido, name='crear_contenido'),
    path('contenidos/editar/<int:id>/',editar_contenido, name='editar_contenido'),
    path('contenidos/confirmar_eliminacion/<int:pk>/',eliminar_contenido, name='eliminar_contenido'),
    path('contenidos/visualizar/<int:id>/',visualizar_contenido, name='visualizar_contenido'),
    path('ajax/load-subcategorias/', cargar_subcategorias, name='ajax_load_subcategorias'),
    path('comentarios/eliminar/<int:comentario_id>/', eliminar_comentario, name='eliminar_comentario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
