from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Contenidos, Estado
from datetime import timedelta
import json


class ReportesViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Inicializa el cliente para realizar peticiones
        Estado.objects.get_or_create(descripcion="Publicado")
        cls.client = Client()
        cls.fecha_actual = timezone.now().date()
        cls.fecha_inicio = cls.fecha_actual - timedelta(days=10)
        cls.fecha_fin = cls.fecha_actual

        # Obtén los estados creados por el signal
        cls.estado_publicado = Estado.objects.get(descripcion="Publicado")
        cls.estado_inactivo = Estado.objects.get(descripcion="Inactivo")
        cls.estado_borrador = Estado.objects.get(descripcion="Borrador")

        # Crear contenidos de prueba con los estados iniciales
        Contenidos.objects.create(
            titulo="Contenido Publicado",
            fecha_creacion=cls.fecha_inicio,
            fecha_publicacion=cls.fecha_actual,
            numero_lecturas=50,
            estado=cls.estado_publicado
        )
        Contenidos.objects.create(
            titulo="Contenido Inactivo",
            fecha_creacion=cls.fecha_inicio,
            fecha_de_inactivacion=cls.fecha_actual,
            estado=cls.estado_inactivo
        )
        Contenidos.objects.create(
            titulo="Contenido Borrador",
            fecha_creacion=cls.fecha_inicio,
            estado=cls.estado_borrador
        )

    def test_reporte_contenidos_mas_leidos(self):
        response = self.client.post(reverse('reporte_contenidos_mas_leidos'), {
            'fecha_inicio': self.fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_fin': self.fecha_fin.strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('graph_json', response.context)
        graph_data = json.loads(response.context['graph_json'])
        self.assertEqual(graph_data['data'][0]['type'], 'bar')
        self.assertEqual(graph_data['data'][0]['x'][0], 'Contenido Publicado')

    def test_reporte_contenidos_publicados_rechazados(self):
        response = self.client.post(reverse('reporte_contenidos_publicados_rechazados'), {
            'fecha_inicio': self.fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_fin': self.fecha_fin.strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('graph_json', response.context)
        self.assertIn("Publicados", response.context['graph_json'])
        self.assertIn("Rechazados", response.context['graph_json'])

    def test_reporte_promedio_tiempo_revision(self):
        response = self.client.post(reverse('reporte_promedio_tiempo_revision'), {
            'fecha_inicio': self.fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_fin': self.fecha_fin.strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('graph_json', response.context)
        self.assertIn('contenidos_tiempos', response.context)
        self.assertIn('promedio_tiempo', response.context)
        self.assertTrue(isinstance(response.context['contenidos_tiempos'], list))
        self.assertIsNotNone(response.context['promedio_tiempo'])

    def test_reporte_contenidos_inactivos(self):
        response = self.client.post(reverse('reporte_contenidos_inactivos'), {
            'fecha_inicio': self.fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_fin': self.fecha_fin.strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('graph_json', response.context)
        self.assertIn("Activos", response.context['graph_json'])
        self.assertIn("Inactivos", response.context['graph_json'])

    def test_reporte_principal(self):
        response = self.client.get(reverse('reporte_principal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reporte_principal.html')
