# Configuration file for the Sphinx documentation builder.

import os
import sys
import django
from django.conf import settings

# Agregar el directorio del proyecto Django al path
sys.path.insert(0, os.path.abspath('..'))

# Configura el módulo de ajustes de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')

# Configura Django
django.setup()

# -- Project information -----------------------------------------------------
project = 'CMS'
copyright = '2024, Equipo5'
author = 'Equipo5'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_use_index = True
html_search = True
