from django.test import TestCase
from Categoria.models import Categoria, Subcategoria

class SubcategoriaModelTest(TestCase):
    def setUp(self):
        """Configurar los datos iniciales para las pruebas."""
        # Crear una instancia de Categoria
        self.categoria = Categoria.objects.create(
            nombre='Categoria Test',
            descripcion='Esta es una descripción de prueba'
        )

        # Crear una instancia de Subcategoria vinculada a la categoría creada
        self.subcategoria = Subcategoria.objects.create(
            nombre='Subcategoria Test',
            descripcion='Descripción de subcategoría de prueba',
            categoriaPadre=self.categoria
        )

    def test_subcategoria_creation(self):
        """Probar la creación de la instancia de Subcategoria."""
        # Verificar que los campos de Subcategoria se asignan correctamente
        self.assertEqual(self.subcategoria.nombre, 'Subcategoria Test')
        self.assertEqual(self.subcategoria.descripcion, 'Descripción de subcategoría de prueba')
        self.assertEqual(self.subcategoria.categoriaPadre, self.categoria)

    def test_str_method(self):
        """Probar el método __str__ de Subcategoria."""
        # Verificar que el método __str__ devuelva el nombre de la subcategoría
        self.assertEqual(str(self.subcategoria), 'Subcategoria Test')

    def test_subcategoria_null_categoriaPadre(self):
        """Probar la creación de una Subcategoria sin categoriaPadre."""
        # Crear una Subcategoria sin especificar categoriaPadre
        subcategoria_sin_padre = Subcategoria.objects.create(
            nombre='Subcategoria Sin Padre',
            descripcion='Descripción sin categoría padre'
        )
        # Verificar que el campo categoriaPadre sea nulo
        self.assertIsNone(subcategoria_sin_padre.categoriaPadre)

    def test_subcategoria_deletion(self):
        """Probar la eliminación de una Subcategoria."""
        # Eliminar la subcategoría
        self.subcategoria.delete()
        # Verificar que ya no existe
        with self.assertRaises(Subcategoria.DoesNotExist):
            Subcategoria.objects.get(id=self.subcategoria.id)

    def test_categoria_deletion_cascade(self):
        """Probar que al eliminar una Categoria se eliminan sus Subcategorias."""
        # Eliminar la categoría
        self.categoria.delete()
        # Verificar que la subcategoría asociada también se elimina
        with self.assertRaises(Subcategoria.DoesNotExist):
            Subcategoria.objects.get(id=self.subcategoria.id)
