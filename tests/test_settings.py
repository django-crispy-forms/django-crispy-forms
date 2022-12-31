import os

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "crispy_forms",
    "tests",
    "crispy_bootstrap3",
    "crispy_bootstrap4",
)

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
)

ROOT_URLCONF = "tests.urls"
CRISPY_CLASS_CONVERTERS = {"textinput": "textinput textInput inputtext"}
CRISPY_TEMPLATE_PACK = "bootstrap3"
SECRET_KEY = "secretkey"
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
USE_TZ = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"),)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": TEMPLATE_DEBUG,
        },
    },
]
