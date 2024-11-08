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
import os



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
        self.assertEqual(len(form.errors), 3)  # Verificar que hay errores para título, contenido y estado



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