from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from .models import Contenidos, Estado, Categoria, Subcategoria, Comentario
from .forms import ContenidosForm, EditarContenidosForm, ComentarioForm
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
            titulo="Título de prueba",
            contenido="Contenido de prueba",
            categoria=self.categoria,
            plantilla=self.plantilla,
            estado=self.estado
        )

    def test_contenidos_creation(self):
        self.assertEqual(self.contenido.titulo, "Título de prueba")
        self.assertEqual(self.contenido.autor.username, "testuser")
        self.assertEqual(self.contenido.estado.descripcion, "Publicado")

    def test_contenidos_str_method(self):
        self.assertEqual(str(self.contenido), "Título de prueba")


class ContenidosFormTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Categoría de prueba")
        self.subcategoria = Subcategoria.objects.create(nombre="Subcategoría de prueba", categoriaPadre=self.categoria)
        self.estado = Estado.objects.create(descripcion="Publicado")

    def test_form_valid_data(self):
        form_data = {
            'titulo': 'Nuevo contenido',
            'contenido': 'Contenido detallado',
            'categoria': self.categoria.id,
            'subcategoria': self.subcategoria.id,
            'estado': self.estado.id,
        }
        form = ContenidosForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            'titulo': '',  # Sin título
            'contenido': '',
            'categoria': self.categoria.id,
            'subcategoria': self.subcategoria.id,
            'estado': self.estado.id,
        }
        form = ContenidosForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Debería haber 2 errores (en título y contenido)


class ContenidosViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.estado = Estado.objects.create(descripcion="Publicado")
        self.categoria = Categoria.objects.create(nombre="Categoría de prueba")
        self.subcategoria = Subcategoria.objects.create(nombre="Subcategoría de prueba", categoriaPadre=self.categoria)

        self.contenido = Contenidos.objects.create(
            titulo="Título de prueba",
            contenido="Contenido de prueba",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            estado=self.estado,
            autor=self.user,
        )

        self.user.user_permissions.add(Permission.objects.get(codename='view_contenidos'))

    def test_contenidos_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('contenidos'))  # Verificar que se puede acceder a la vista de contenidos
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Título de prueba")
        self.assertTemplateUsed(response, 'contenidos/contenidos.html')

    def test_crear_contenido_view(self):
        self.client.login(username='testuser', password='12345')
        self.user.user_permissions.add(Permission.objects.get(codename='add_contenidos'))

        form_data = {
            'titulo': 'Nuevo contenido',
            'contenido': 'Contenido de prueba',
            'categoria': self.categoria.id,
            'subcategoria': self.subcategoria.id,
            'estado': self.estado.id
        }
        response = self.client.post(reverse('crear_contenido'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear el contenido
        self.assertTrue(Contenidos.objects.filter(titulo='Nuevo contenido').exists())  # Verificar que el contenido fue creado

    def test_eliminar_contenido(self):
        self.client.login(username='testuser', password='12345')
        self.user.user_permissions.add(Permission.objects.get(codename='delete_contenidos'))

        response = self.client.post(reverse('eliminar_contenido', args=[self.contenido.id]))
        self.assertEqual(response.status_code, 302)  # Redirección tras eliminar
        self.assertFalse(Contenidos.objects.filter(id=self.contenido.id).exists())  # El contenido ya no debe existir

class ComentarioFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.estado = Estado.objects.create(descripcion="Publicado")
        self.categoria = Categoria.objects.create(nombre="Categoría de prueba")
        self.contenido = Contenidos.objects.create(
            titulo="Título de prueba",
            contenido="Contenido de prueba",
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

