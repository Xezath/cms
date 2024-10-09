from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from Usuario.forms import GroupForm, GroupEditForm
from Usuario.forms import CustomAdminUserChangeForm
from Categoria.models import Categoria
from django.contrib.contenttypes.models import ContentType

class RegistrarTest(TestCase):
    
    def test_registrar_get(self):
        response = self.client.get(reverse('registrar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registrar.html')

    def test_registrar_post_success(self):
        response = self.client.post(reverse('registrar'), {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email':'testemail@gmail.com'
        })
        self.assertRedirects(response, reverse('exito'))
        self.assertTrue(User.objects.filter(username='newuser').exists())


class IniciarSesionTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_iniciar_sesion_get(self):
        response = self.client.get(reverse('Iniciar_Sesion'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Iniciar_Sesion.html')

    def test_iniciar_sesion_post_success(self):
        response = self.client.post(reverse('Iniciar_Sesion'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, reverse('home'))

    def test_iniciar_sesion_post_failure(self):
        response = self.client.post(reverse('Iniciar_Sesion'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Iniciar_Sesion.html')
        self.assertContains(response, 'Username or password is incorrect')

class RolePermissionTest(TestCase):

    def setUp(self):
        # Crear usuarios
        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.suscriptor_user = User.objects.create_user(username='suscriptor', password='suscriptorpass')
        self.autor_user = User.objects.create_user(username='autor', password='autorpass')

        # Crear grupos (roles)
        self.admin_group = Group.objects.create(name='Administrador')
        self.suscriptor_group = Group.objects.create(name='Suscriptor')
        self.autor_group = Group.objects.create(name='Autor')

        # Obtener permisos autogenerados para el modelo "Categoria"
        categoria_content_type = ContentType.objects.get_for_model(Categoria)
        add_perm = Permission.objects.get(codename='add_categoria', content_type=categoria_content_type)
        change_perm = Permission.objects.get(codename='change_categoria', content_type=categoria_content_type)
        delete_perm = Permission.objects.get(codename='delete_categoria', content_type=categoria_content_type)
        view_perm = Permission.objects.get(codename='view_categoria', content_type=categoria_content_type)

        # Asignar permisos al grupo Administrador
        self.admin_group.permissions.add(add_perm, change_perm, delete_perm, view_perm)

        # Asignar permisos al grupo Autor (puede ver y agregar categorías)
        self.autor_group.permissions.add(add_perm, view_perm)

        # Asignar usuarios a los grupos
        self.admin_user.groups.add(self.admin_group)
        self.suscriptor_user.groups.add(self.suscriptor_group)
        self.autor_user.groups.add(self.autor_group)

    def test_admin_can_add_edit_delete_view_categoria(self):
        self.client.login(username='admin', password='adminpass')

        # Verificar que el administrador puede acceder a la vista de creación
        response = self.client.get(reverse('crear_cat'))
        self.assertEqual(response.status_code, 200)

        # Probar la creación de una categoría
        response = self.client.post(reverse('crear_cat'), {
            'nombre': 'Categoria Admin',
            'descripcion': 'Descripción creada por admin'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Categoria.objects.filter(nombre='Categoria Admin').exists())

        # Probar la edición de la categoría
        categoria = Categoria.objects.get(nombre='Categoria Admin')
        response = self.client.post(reverse('editar_cat', args=[categoria.id]), {
            'nombre': 'Categoria Admin Editada',
            'descripcion': 'Descripción editada por admin'
        })
        self.assertEqual(response.status_code, 302)
        categoria.refresh_from_db()
        self.assertEqual(categoria.nombre, 'Categoria Admin Editada')

        # Probar la eliminación de la categoría
        response = self.client.post(reverse('borrar_cat', args=[categoria.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Categoria.objects.filter(id=categoria.id).exists())

        # Probar la visualización de categorías
        response = self.client.get(reverse('categorias'))
        self.assertEqual(response.status_code, 200)

    def test_autor_can_add_and_view_categoria_but_cannot_edit_or_delete(self):
        self.client.login(username='autor', password='autorpass')

        # Verificar que el autor puede acceder a la vista de creación
        response = self.client.get(reverse('crear_cat'))
        self.assertEqual(response.status_code, 200)

        # Probar la creación de una categoría
        response = self.client.post(reverse('crear_cat'), {
            'nombre': 'Categoria Autor',
            'descripcion': 'Descripción creada por autor'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Categoria.objects.filter(nombre='Categoria Autor').exists())

        # Probar que el autor no puede acceder a la vista de edición
        categoria = Categoria.objects.get(nombre='Categoria Autor')
        response = self.client.get(reverse('editar_cat', args=[categoria.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Probar que el autor no puede eliminar la categoría
        response = self.client.post(reverse('borrar_cat', args=[categoria.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Probar la visualización de categorías
        response = self.client.get(reverse('categorias'))
        self.assertEqual(response.status_code, 200)

    def test_suscriptor_cannot_add_edit_delete_but_can_view_categoria(self):
        self.client.login(username='suscriptor', password='suscriptorpass')

        # Verificar que el suscriptor no puede acceder a la vista de creación
        response = self.client.get(reverse('crear_cat'))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Verificar que el suscriptor no puede acceder a la vista de edición
        categoria = Categoria.objects.create(nombre='Categoria Suscriptor', descripcion='Descripción')
        response = self.client.get(reverse('editar_cat', args=[categoria.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Verificar que el suscriptor no puede eliminar la categoría
        response = self.client.post(reverse('borrar_cat', args=[categoria.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Probar la visualización de categorías
        response = self.client.get(reverse('categorias'))
        self.assertNotEqual(response.status_code, 200)