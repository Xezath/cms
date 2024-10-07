from django.urls import path
from . import views

app_name = 'kanban'

urlpatterns = [
    path('actualizar_estado/<int:tarjeta_id>/<str:nuevo_estado>/', views.actualizar_estado, name='actualizar_estado'),
    path('tablero/<int:tablero_id>/', views.tablero_kanban, name='tablero_kanban'),
]
