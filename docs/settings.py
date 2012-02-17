import os

SITE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (os.path.join(SITE_ROOT, 'templates'))

INSTALLED_APPS = (
    'crispy_forms'
)
