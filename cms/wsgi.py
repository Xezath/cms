"""
Configuración de WSGI para el proyecto CMS.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')

application = get_wsgi_application()
