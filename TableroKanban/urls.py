from django.urls import path
from . import views

app_name = 'kanban'

urlpatterns = [
    path('tablero/<int:tablero_id>/', views.tablero_kanban, name='tablero_kanban'),
]
