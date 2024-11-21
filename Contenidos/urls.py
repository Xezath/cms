from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import aceptar_rechazar_contenido, contenidos, crear_contenido, editar_contenido, eliminar_contenido, enviar_a_revision, publicar_contenido, visualizar_contenido, cargar_subcategorias, eliminar_comentario, visualizar_contenido_aceptado, visualizar_contenido_borrador, visualizar_contenido_revision, ver_historial

urlpatterns = [
    path('contenidos/', contenidos, name='contenidos'),
    path('contenidos/crear/', crear_contenido, name='crear_contenido'),
    path('contenidos/editar/<int:id>/',editar_contenido, name='editar_contenido'),
    path('contenidos/confirmar_eliminacion/<int:pk>/',eliminar_contenido, name='eliminar_contenido'),
    path('contenidos/visualizar/<int:id>/',visualizar_contenido, name='visualizar_contenido'),
    path('ajax/load-subcategorias/', cargar_subcategorias, name='ajax_load_subcategorias'),
    path('comentarios/eliminar/<int:comentario_id>/', eliminar_comentario, name='eliminar_comentario'),
    path('contenidos/borrador/<int:id>/',visualizar_contenido_borrador, name='visualizar_contenido_borrador'),
    path('contenidos/revision/<int:id>/',visualizar_contenido_revision, name='visualizar_contenido_revision'),
    path('contenidos/aceptado/<int:id>/',visualizar_contenido_aceptado, name='visualizar_contenido_aceptado'),
    path('enviar-a-revision/<int:id>/', enviar_a_revision, name='enviar_a_revision'),
    path('aceptar-rechazar-contenido/<int:id>/', aceptar_rechazar_contenido, name='aceptar_rechazar_contenido'),
    path('publicar-contenido/<int:id>/', publicar_contenido, name='publicar_contenido'),
    path('contenidos/historial/<int:id>',ver_historial, name= 'ver_historial')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
