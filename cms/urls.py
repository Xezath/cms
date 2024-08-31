"""
URL configuration for cms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from Usuario import views
from django.urls import path, re_path
from django.urls import include



urlpatterns = [

    path('admin/',admin.site.urls),
    path('', views.home, name='home'),  # URL para la página principal
    path('registrar/', views.registrar, name='registrar'),  # URL para el registro
    path('exito/', views.exito, name='exito'),
    path('home/',views.home, name='home'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('signin/', views.Iniciar_Sesion, name='Iniciar_Sesion'),
    path('categoria/', include('Categoria.urls')),
    path('plantilla/', include('Plantilla.urls')),
   
]
