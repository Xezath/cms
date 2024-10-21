from django.test import TestCase
from django.utils import timezone
from Contenidos.models import Contenidos, Estado
from Categoria.models import Categoria
from Plantilla.models import Plantilla, Color, Margenes

class ContenidosModelTest(TestCase):
    def setUp(self):
        """Setup initial data for tests."""
        # Elimina los datos antiguos antes de crear nuevos
        Estado.objects.all().delete()
        # Create instances of Categoria and Margenes
        self.categoria = Categoria.objects.create(nombre='Categoria Test')
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
        self.plantilla = Plantilla.objects.create(
            nombre='Plantilla Test',
            descripcion='Descripción de prueba',
            colorFondo=self.color,
            margenes=self.margenes,
            disposicionHorizontal=True
        )

        self.estado, created = Estado.objects.get_or_create(descripcion='Activo')
        
        # Create a Contenidos instance
        self.contenido = Contenidos.objects.create(
            titulo='Contenido Test',
            contenido='Este es un contenido de prueba.',
            fecha_creacion=timezone.now(),
            categoria=self.categoria,
            plantilla=self.plantilla,
            estado=self.estado
        )
    
    def test_contenidos_creation(self):
        """Test the creation of Contenidos instance."""
        self.assertEqual(self.contenido.titulo, 'Contenido Test')
        self.assertEqual(self.contenido.contenido, 'Este es un contenido de prueba.')
        self.assertEqual(self.contenido.categoria, self.categoria)
        self.assertEqual(self.contenido.plantilla, self.plantilla)
        self.assertIsNotNone(self.contenido.fecha_creacion)

    def test_str_method(self):
        """Test the __str__ method of Contenidos.""" 
        self.assertEqual(str(self.contenido), 'Contenido Test')

    def test_default_fecha_creacion(self):
        """Test that fecha_creacion is set to the current time by default."""
        contenido = Contenidos.objects.create(
            titulo='Otro Contenido Test',
            contenido='Este es otro contenido de prueba.',
            categoria=self.categoria,
            plantilla=self.plantilla,
            estado=self.estado
        )
        self.assertAlmostEqual(contenido.fecha_creacion, timezone.now(), delta=timezone.timedelta(seconds=1))
    
    def test_permissions(self):
        """Test the permissions defined in the Meta class."""
        self.assertIn(('can_add', 'Puede agregar contenido'), Contenidos._meta.permissions)
        self.assertIn(('can_modify', 'Puede editar contenido'), Contenidos._meta.permissions)
        self.assertIn(('can_delete', 'Puede eliminar contenido'), Contenidos._meta.permissions)
        self.assertIn(('can_viewInactive', 'Puede ver contenido inactivo'), Contenidos._meta.permissions)

