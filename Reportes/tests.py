from django.test import TestCase, RequestFactory
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Contenidos, Estado
from .views import (
    generar_reporte_contenidos_mas_leidos,
    generar_reporte_contenidos_publicados_rechazados,
    generar_reporte_promedio_tiempo_revision,
    generar_reporte_contenidos_inactivos,
    reporte_todos,
)


class ReporteTestCase(TestCase):
    def setUp(self):
        # Crear estados
        self.estado_activo = Estado.objects.create(descripcion="Activo")
        self.estado_inactivo = Estado.objects.create(descripcion="Inactivo")
        self.estado_rechazado = Estado.objects.create(descripcion="Rechazado")

        # Crear contenidos
        self.fecha_hoy = datetime.now()
        self.fecha_pasada = self.fecha_hoy - timedelta(days=10)

        self.contenido1 = Contenidos.objects.create(
            titulo="Contenido 1",
            estado=self.estado_activo,
            fecha_publicacion=self.fecha_hoy,
            numero_lecturas=100,
        )
        self.contenido2 = Contenidos.objects.create(
            titulo="Contenido 2",
            estado=self.estado_inactivo,
            fecha_de_inactivacion=self.fecha_hoy,
            numero_lecturas=50,
        )
        self.contenido3 = Contenidos.objects.create(
            titulo="Contenido 3",
            estado=self.estado_rechazado,
            fecha_de_rechazados=self.fecha_hoy,
            numero_lecturas=25,
        )

    def test_generar_reporte_contenidos_mas_leidos(self):
        fecha_inicio = self.fecha_pasada
        fecha_fin = self.fecha_hoy
        div = generar_reporte_contenidos_mas_leidos(fecha_inicio, fecha_fin)

        self.assertIn("Contenido 1", div)
        self.assertIn("100", div)
        self.assertNotIn("Contenido 2", div)  # Contenidos con menos lecturas no aparecen

    def test_generar_reporte_contenidos_publicados_rechazados(self):
        fecha_inicio = self.fecha_pasada
        fecha_fin = self.fecha_hoy
        div = generar_reporte_contenidos_publicados_rechazados(fecha_inicio, fecha_fin)

        self.assertIn("Publicados", div)
        self.assertIn("Rechazados", div)
        self.assertIn("1", div)  # Cantidad de publicados
        self.assertIn("1", div)  # Cantidad de rechazados

    def test_generar_reporte_promedio_tiempo_revision(self):
        fecha_inicio = self.fecha_pasada
        fecha_fin = self.fecha_hoy
        div = generar_reporte_promedio_tiempo_revision(fecha_inicio, fecha_fin)

        self.assertIn("Promedio", div)
        self.assertIn("h", div)  # Asegurar formato de tiempo
        self.assertIn("m", div)

    def test_generar_reporte_contenidos_inactivos(self):
        fecha_inicio = self.fecha_pasada
        fecha_fin = self.fecha_hoy
        div = generar_reporte_contenidos_inactivos(fecha_inicio, fecha_fin)

        self.assertIn("Inactivos", div)
        self.assertIn("Activos", div)
        self.assertIn("1", div)  # Cantidad de contenidos activos
        self.assertIn("1", div)  # Cantidad de contenidos inactivos

