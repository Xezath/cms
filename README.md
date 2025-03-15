# 📌 Sistema de Gestión de Contenidos (CMS) 

## 📖 Descripción

Este proyecto es un Sistema de Gestión de Contenidos (CMS) desarrollado con Django. Permite la creación, edición, revisión y publicación de artículos, así como la administración de usuarios y roles con distintos niveles de permisos. También incluye funcionalidades de notificación y generación de reportes estadísticos sobre el contenido.

## 👥 Integrantes

- Maria Celeste Pérez Martínez
- Maria Paz Sánchez Salinas
- Jazmín Madeline Irazusta Frutos
- Jaime Núñez Viedma

## 🚀 Características principales

- 📂 **Gestión de usuarios y roles:** Administrador, Suscriptor, Autor, Editor y Publicador.
- 📝 **Creación y edición de contenido:** Los usuarios pueden redactar y gestionar artículos.
- 🔄 **Flujo de trabajo de publicación:** Borrador → En Revisión → Publicado.
- 📊 **Reportes estadísticos:** Alcance, artículos más leídos, cantidad de publicaciones, entre otros.
- 📧 **Notificaciones por correo:** Se notifican eventos importantes como envíos a revisión y publicaciones.
- 🔒 **Seguridad y permisos:** Uso de los permisos autogenerados de Django.
- 🎨 **Personalización de interfaz:** Personalizable según las necesidades del usuario.

## 🏗️ Requisitos

- **Python** 3.12.5
- **PostgreSQL** 16

Ejecutando el siguiente comando se instalarán todas las dependencias necesarias:

```bash
pip install -r requirements.txt
```

### 📦 Dependencias principales:

- Django==5.1
- django-allauth==64.2.0
- django-ckeditor==6.7.1
- django-crispy-forms==2.3
- django-keycloak==0.1.1
- django-oauth-toolkit==3.0.1
- djangorestframework==3.15.2
- gunicorn==23.0.0
- pandas==2.2.3
- psycopg2==2.9.10
- requests==2.32.3

(La lista completa de dependencias está en `requirements.txt`)

## ⚙️ Configuración de base de datos

Es necesario configurar correctamente PostgreSQL y asegurarse de que la base de datos esté creada antes de ejecutar la aplicación.
En `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cms',  # Nombre de la base de datos para desarrollo
        'USER': 'postgres',  # Usuario de PostgreSQL
        'PASSWORD': '1234',  # Contraseña de PostgreSQL
        'HOST': 'localhost',
        'PORT': '5432',  # Puerto por defecto de PostgreSQL
    }
}
```

## ▶️ Ejecución del proyecto

Desde el directorio del proyecto, ejecutar los siguientes comandos:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py create_roles
python manage.py runserver
```

Posteriormente, presione `Ctrl` y haga clic en la dirección IP `localhost` que se proporciona al ejecutar el comando.

## ✅ Pruebas

Para ejecutar pruebas unitarias, usa el siguiente comando desde el directorio del proyecto:

```bash
python manage.py test .pruebas_....py
```

Para elegir qué test ejecutar, en la parte de `.test_....py`, escribe el test que deseas realizar. Por ejemplo:

```bash
python manage.py test .pruebas_usuario.py
```







