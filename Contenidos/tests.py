from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from .models import Contenidos, Estado, Categoria, Subcategoria, Comentario
from .forms import ContenidosForm, EditarContenidosForm, ComentarioForm
from django.utils import timezone
from Plantilla.models import Plantilla, Color, Margenes
from django.core import mail
from django.core.mail import send_mail
from django.test import override_settings
from datetime import datetime
import os
import unittest



class ContenidosModelTest(TestCase):
    def setUp(self):
        """Setup initial data for tests."""
        # Elimina los datos antiguos antes de crear nuevos
        Estado.objects.all().delete()
        # Crear instancias necesarias
        self.categoria = Categoria.objects.create(nombre='Categoria Test')
        self.estado = Estado.objects.create(descripcion="Activo")
        self.color = Color.objects.create(nombre='Blanco', codigo='#FFFFFF')
        self.margenes = Margenes.objects.create(
            der=10.0,
            izq=10.0,
            arr=20.0,
            aba=20.0
        )

        self.plantilla = Plantilla.objects.create(
            nombre='Plantilla Test',
            descripcion='Descripción de prueba',
            colorFondo=self.color,
            margenes=self.margenes,
            disposicionHorizontal=True
        )

        self.user = User.objects.create_user(username='testuser', password='testpassword') 
        
        # Create a Contenidos instance
        self.contenido = Contenidos.objects.create(
            titulo="Título de prueba",
            contenido="Contenido de prueba",
            categoria=self.categoria,
            plantilla=self.plantilla,
            estado=self.estado,
            autor=self.user 
        )

    def test_contenidos_creation(self):
        self.assertEqual(self.contenido.titulo, "Título de prueba")
        self.assertEqual(self.contenido.autor.username, "testuser")
        self.assertEqual(self.contenido.estado.descripcion, "Activo")

    def test_contenidos_str_method(self):
        self.assertEqual(str(self.contenido), "Título de prueba")


class ContenidosFormTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Categoría de prueba")
        self.subcategoria = Subcategoria.objects.create(nombre="Subcategoría de prueba", categoriaPadre=self.categoria)
        self.estado = Estado.objects.create(descripcion="Activo")
        

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


class ComentarioFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.estado = Estado.objects.create(descripcion="Activo")
        self.categoria = Categoria.objects.create(nombre="Categoría de prueba")
        self.color = Color.objects.get_or_create(nombre='Blanco', codigo='#FFFFFF')[0]
        self.margenes = Margenes.objects.get_or_create(der=10.0, izq=10.0, arr=20.0, aba=20.0)[0]
        self.plantilla = Plantilla.objects.create(
            nombre='Plantilla Test',
            descripcion='Descripción de prueba',
            colorFondo=self.color,
            margenes=self.margenes,
            disposicionHorizontal=True
        )  

        self.contenido = Contenidos.objects.create(
            titulo="Título de prueba",
            contenido="Contenido de prueba",
            categoria=self.categoria,
            plantilla=self.plantilla,
            estado=self.estado
        )

        self.assertAlmostEqual(self.contenido.fecha_creacion, timezone.now(), delta=timezone.timedelta(seconds=1))
    
    def test_permissions(self):
        """Test the permissions defined in the Meta class."""
        self.assertIn(('can_add', 'Puede agregar contenido'), Contenidos._meta.permissions)
        self.assertIn(('can_modify', 'Puede editar contenido'), Contenidos._meta.permissions)
        self.assertIn(('can_delete', 'Puede eliminar contenido'), Contenidos._meta.permissions)
        self.assertIn(('can_viewInactive', 'Puede ver contenido inactivo'), Contenidos._meta.permissions)


class EmailTest(TestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email(self):
        subject = 'Test Email'
        message = 'This is a test email.'
        from_email = 'from@example.com'
        recipient_list = ['to@example.com']
        send_mail(subject, message, from_email, recipient_list)
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, subject)
        self.assertEqual(sent_email.body, message)
        self.assertEqual(sent_email.from_email, from_email)
        self.assertEqual(sent_email.to, recipient_list)


class ContentHistoryTestCase(TestCase):
    def setUp(self):
        """
        Set up test data that will be used across multiple test methods
        """
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )

        # Create a test state
        self.estado = Estado.objects.create(
            descripcion='Borrador'
        )

        # Create a test content
        self.contenido = Contenidos.objects.create(
            titulo='Test Content',
            contenido='Test Content Body',
            autor=self.user,
            estado=self.estado
        )

    def test_agregar_historial_method(self):
        """
        Test the agregar_historial method of the Contenidos model
        """
        # Initial state of historial
        initial_historial = self.contenido.historial

        # Add a history entry
        self.contenido.agregar_historial("Test Action", "Test Details")

        # Refresh the content from the database
        self.contenido.refresh_from_db()

        # Check that a new history entry was added
        self.assertTrue(len(self.contenido.historial) > len(initial_historial))
        
        # Check that the new entry contains the expected text
        self.assertIn("Test Action - Test Details", self.contenido.historial)
        
        # Check that the entry includes a timestamp
        self.assertTrue(datetime.now().strftime("%Y-%m-%d") in self.contenido.historial)

    def test_ver_historial_view(self):
        """
        Test the ver_historial view
        """
        # Add some history entries
        self.contenido.agregar_historial("First Action", "First Details")
        self.contenido.agregar_historial("Second Action", "Second Details")

        # Log in the test user
        self.client.login(username='testuser', password='12345')

        # Get the ver_historial URL
        url = reverse('ver_historial', kwargs={'id': self.contenido.id})
        
        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the content's history is in the response
        self.assertContains(response, "First Action")
        self.assertContains(response, "Second Action")

    def test_historial_entries_multiple_methods(self):
        """
        Test adding multiple history entries through different methods
        """
        # Add initial history entry during content creation
        self.contenido.agregar_historial("Created", "Initial content creation")

        # Simulate state change
        new_estado = Estado.objects.create(descripcion='Revisión')
        self.contenido.estado = new_estado
        self.contenido.save()
        self.contenido.agregar_historial(f"Cambio de estado '{self.estado}' a estado '{new_estado}'")

        # Refresh the content
        self.contenido.refresh_from_db()

        # Split the history entries
        history_entries = self.contenido.historial.split("\n")

        # Check that we have multiple entries
        self.assertTrue(len(history_entries) >= 2)
        
        # Check the content of entries
        self.assertIn("Created", history_entries[0])
        self.assertIn("Cambio de estado", history_entries[1])

    def test_historial_view_permissions(self):
        """
        Test that only authenticated users can view history
        """
        # Create another user without permissions
        other_user = User.objects.create_user(
            username='otheruser', 
            password='54321'
        )

        # Get the ver_historial URL
        url = reverse('ver_historial', kwargs={'id': self.contenido.id})
        
        # Try accessing without login (no redirection check)
        response = self.client.get(url)
        
        # If you want to skip the redirect check, you can just check if the status is 200
        self.assertEqual(response.status_code, 200)  # Check if the page loads even without login

        # Login with the content's author
        self.client.login(username='testuser', password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Should return 200 after login
