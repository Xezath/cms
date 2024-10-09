from django.test import TestCase
from Plantilla.models import Plantilla, Margenes, Color

class PlantillaModelTest(TestCase):
    def setUp(self):
        """Configura los datos iniciales para las pruebas."""
        # Crea instancias de Margenes y Color
        self.margenes = Margenes.objects.create(
            der=10.0,
            izq=10.0,
            arr=20.0,
            aba=20.0
        )
        self.color = Color.objects.create(
            nombre='Blanco',
            codigo='#FFFFFF'
        )
        # Crea una instancia de Plantilla
        self.plantilla = Plantilla.objects.create(
            nombre='Plantilla Test',
            descripcion='Descripción de prueba',
            colorFondo=self.color,
            margenes=self.margenes,
            disposicionHorizontal=True
        )

    def test_plantilla_creation(self):
        """Prueba la creación de la instancia Plantilla."""
        self.assertEqual(self.plantilla.nombre, 'Plantilla Test')
        self.assertEqual(self.plantilla.descripcion, 'Descripción de prueba')
        self.assertEqual(self.plantilla.colorFondo, self.color)
        self.assertEqual(self.plantilla.margenes, self.margenes)
        self.assertTrue(self.plantilla.disposicionHorizontal)

    def test_str_method(self):
        """Prueba el método __str__ de Plantilla."""
        self.assertEqual(str(self.plantilla), 'Plantilla Test')

    def test_plantilla_deletion(self):
        """Prueba la eliminación de una Plantilla."""
        self.plantilla.delete()
        with self.assertRaises(Plantilla.DoesNotExist):
            Plantilla.objects.get(id=self.plantilla.id)

    def test_margenes_str_method(self):
        """Prueba el método __str__ de Margenes."""
        self.assertEqual(str(self.margenes), '10.0')

    def test_color_str_method(self):
        """Prueba el método __str__ de Color."""
        self.assertEqual(str(self.color), 'Blanco')
