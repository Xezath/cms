from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Tablero, Columna, Tarjeta
from Contenidos.models import Estado, Contenidos
from django.urls import reverse


class TableroKanbanModelTests(TestCase):
    
    def setUp(self):
        # Crear usuario y grupos
        self.user = User.objects.create_user(username='autor', password='12345')
        self.admin_group = Group.objects.create(name='Administrador')
        self.user.groups.add(self.admin_group)
        
        # Crear estados
        self.activo = Estado.objects.create(descripcion='Activo')
        self.inactivo = Estado.objects.create(descripcion='Inactivo')
        
        # Crear tablero
        self.tablero = Tablero.objects.create(nombre="Tablero de prueba")
        
        # Crear columnas
        self.columna_activa = Columna.objects.create(nombre="Columna Activa", tablero=self.tablero, estado=self.activo, orden=1)
        self.columna_inactiva = Columna.objects.create(nombre="Columna Inactiva", tablero=self.tablero, estado=self.inactivo, orden=2)
        
        # Crear contenido
        self.contenido = Contenidos.objects.create(titulo="Contenido de prueba", estado=self.activo)
        
        # Crear tarjeta
        self.tarjeta = Tarjeta.objects.create(
            contenido=self.contenido, 
            autor=self.user, 
            columna=self.columna_activa, 
            titulo="Tarjeta de prueba", 
            estado=self.activo, 
            orden=1
        )
    
    def test_tarjeta_se_crea_correctamente(self):
        self.assertEqual(self.tarjeta.titulo, "Tarjeta de prueba")
        self.assertEqual(self.tarjeta.estado, self.activo)
        self.assertEqual(self.tarjeta.columna, self.columna_activa)

    def test_tarjeta_se_mueve_a_columna_correcta_por_estado(self):
        self.tarjeta.estado = self.inactivo
        self.tarjeta.save()
        self.tarjeta.refresh_from_db()
        self.assertEqual(self.tarjeta.columna, self.columna_inactiva)

class TableroKanbanViewTests(TestCase):
    
    def setUp(self):
        # Crear usuario y grupos
        self.user = User.objects.create_user(username='autor', password='12345')
        self.admin_group = Group.objects.create(name='Administrador')
        self.user.groups.add(self.admin_group)
        
        # Crear estados
        self.activo = Estado.objects.create(descripcion='Activo')
        self.inactivo = Estado.objects.create(descripcion='Inactivo')
        
        # Crear tablero
        self.tablero = Tablero.objects.create(nombre="Tablero de prueba")
        
        # Crear columnas
        self.columna_activa = Columna.objects.create(nombre="Columna Activa", tablero=self.tablero, estado=self.activo, orden=1)
        self.columna_inactiva = Columna.objects.create(nombre="Columna Inactiva", tablero=self.tablero, estado=self.inactivo, orden=2)
        
        # Crear contenido y tarjeta
        self.contenido = Contenidos.objects.create(titulo="Contenido de prueba", estado=self.activo)
        self.tarjeta = Tarjeta.objects.create(contenido=self.contenido, autor=self.user, columna=self.columna_activa, titulo="Tarjeta de prueba", estado=self.activo, orden=1)
        
        # Autenticar usuario
        self.client.login(username='autor', password='12345')
    
    def test_acceso_a_tablero_kanban(self):
        url = reverse('tablero_kanban', args=[self.tablero.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'TableroKanban/tablero.html')

    def test_tarjetas_filtradas_por_estado(self):
        url = reverse('tablero_kanban', args=[self.tablero.id])
        response = self.client.get(url)
        self.assertContains(response, 'Tarjeta de prueba')  # La tarjeta activa debe estar presente
