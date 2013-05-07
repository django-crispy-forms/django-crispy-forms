import os

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'crispy_forms',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'
CRISPY_TEMPLATE_PACK = 'bootstrap'
CRISPY_CLASS_CONVERTERS = {"textinput": "textinput textInput inputtext"}
SECRET_KEY = 'secretkey'

# http://djangosnippets.org/snippets/646/
class InvalidVarException(object):
    def __mod__(self, missing):
        try:
            missing_str = unicode(missing)
        except:
            missing_str = 'Failed to create string representation'
        raise Exception('Unknown template variable %r %s' % (missing, missing_str))

    def __contains__(self, search):
        if search == '%s':
            return True
        return False

TEMPLATE_DEBUG = True
TEMPLATE_STRING_IF_INVALID = InvalidVarException()
