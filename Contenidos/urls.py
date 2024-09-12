from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import contenidos, crear_contenido, editar_contenido, eliminar_contenido, visualizar_contenido

urlpatterns = [
    path('contenidos/', contenidos, name='contenidos'),
    path('contenidos/crear/', crear_contenido, name='crear_contenido'),
    path('contenidos/editar/<int:pk>/',editar_contenido, name='editar_contenido'),
    path('contenidos/confirmar_eliminacion/<int:pk>/',eliminar_contenido, name='eliminar_contenido'),
    path('contenidos/visualizar/<int:pk>/',visualizar_contenido, name='visualizar_contenido'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
