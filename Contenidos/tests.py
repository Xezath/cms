from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Contenidos, Estado, Categoria, Subcategoria, Comentario
from .forms import ContenidosForm, EditarContenidosForm, ComentarioForm
from django.utils import timezone
from django.contrib.auth.models import Permission

class ContenidosModelTest(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Crear estado y categorías de prueba
        self.estado = Estado.objects.create(descripcion="Publicado")
        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.subcategoria = Subcategoria.objects.create(nombre="Programación", categoriaPadre=self.categoria)

        # Crear contenido de prueba
        self.contenido = Contenidos.objects.create(
            titulo="Título de prueba",
            contenido="Contenido de prueba",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            estado=self.estado,
            autor=self.user,
            fecha_creacion=timezone.now()
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
            estado=self.estado,
            autor=self.user,
        )

    def test_comentario_form_valid(self):
        form_data = {'comentario': 'Este es un comentario de prueba'}
        form = ComentarioForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comentario_form_invalid(self):
        form_data = {'comentario': ''}
        form = ComentarioForm(data=form_data)
        self.assertFalse(form.is_valid())

