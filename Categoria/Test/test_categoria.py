from django.test import TestCase
from Categoria.models import Categoria

class CategoriaModelTest(TestCase):
    def setUp(self):
        """Setup initial data for tests."""
        # Crear una instancia de Categoria
        self.categoria = Categoria.objects.create(
            nombre='Categoria Test',
            descripcion='Esta es una descripción de prueba'
        )

    def test_categoria_creation(self):
        """Test the creation of Categoria instance."""
        # Verificar que los campos de la categoría se asignan correctamente
        self.assertEqual(self.categoria.nombre, 'Categoria Test')
        self.assertEqual(self.categoria.descripcion, 'Esta es una descripción de prueba')

    def test_str_method(self):
        """Test the __str__ method of Categoria."""
        # Verificar el método __str__
        self.assertEqual(str(self.categoria), 'Categoria Test')

    def test_default_fields(self):
        """Test default values and required fields."""
        # Verificar que el campo descripción puede ser null
        categoria_sin_descripcion = Categoria.objects.create(
            nombre='Categoria Sin Descripción'
        )
        self.assertIsNone(categoria_sin_descripcion.descripcion)

    def test_categoria_edit(self):
        """Test editing an existing Categoria."""
        # Editar una categoría existente
        self.categoria.nombre = 'Categoria Editada'
        self.categoria.descripcion = 'Descripción editada'
        self.categoria.save()
        
        # Volver a obtener la categoría y verificar los cambios
        categoria_editada = Categoria.objects.get(id=self.categoria.id)
        self.assertEqual(categoria_editada.nombre, 'Categoria Editada')
        self.assertEqual(categoria_editada.descripcion, 'Descripción editada')

    def test_categoria_deletion(self):
        """Test deleting a Categoria."""
        # Eliminar la categoría
        self.categoria.delete()

        # Verificar que la categoría no existe más
        with self.assertRaises(Categoria.DoesNotExist):
            Categoria.objects.get(id=self.categoria.id)
