"""
Este archivo contiene la configuración de Django para el proyecto CMS.

Incluye configuraciones de bases de datos, aplicaciones instaladas, autenticación y otros ajustes específicos del entorno.
"""

from pathlib import Path
import os
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9o6p%u5$u5z65s$1p&)yy18dabfiwwn-fjwl)q%s*@67whabd9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',

]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.openid_connect',
    'mozilla_django_oidc',
    "crispy_forms",
    "crispy_bootstrap5",
    'ckeditor',
    'ckeditor_uploader',
    'oauth2_provider',
    'Usuario',
    'Categoria',
    'Plantilla',
    'Contenidos',
    'TableroKanban',
    'Reportes',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
SITE_ID = 1

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 36000,
}

# Keycloak settings
KEYCLOAK_SERVER_URL = 'http://localhost:8080/auth/'
KEYCLOAK_REALM = 'sso-login'
KEYCLOAK_CLIENT_ID = 'sso-login-django'
KEYCLOAK_CLIENT_SECRET = 'yAPWogweSFGNoC7trXNA0jR0wtr1z5WZ'
KEYCLOAK_REDIRECT_URI = 'http://localhost:8000/complete/keycloak/'


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full', 
        'width': '100%',
        'height': 300,
        'removePlugins': 'stylesheetparser', 
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'cms.urls'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = 'uploads/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Provider specific settings

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# settings.py
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'poner aqui el client id'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'poner aqui el secret'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'secret': SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'key': ''
        },
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
        'SCOPE': [
            'profile',
            'email'
        ],
    },
    'github': {

        'APP': {
            'client_id': 'Ov23li8dMzjZDjBi8NWh',
            'secret': 'd1737349fcd0751ce89bf4ac9ab6eb219db8a1ba',
            'key': ''
        }
    }
}





WSGI_APPLICATION = 'cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cms',
        'USER': 'postgres',  
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',  # puerto por defecto de PostgreSQL
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cmseq052024@gmail.com'  
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [

]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_TZ = False




STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), 
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




#esto son cosas de estilos
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"