from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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


from django.test import TestCase
from django.contrib.auth.models import User, Group

class UserRoleTest(TestCase):
    def test_first_user_is_superuser(self):
        User.objects.create_user(username='testuser', password='testpassword')
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
