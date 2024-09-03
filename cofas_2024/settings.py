

from pathlib import Path
import os

from django.templatetags.static import static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]
MAX_UPLOAD_SIZE = 5242880  # 5MB

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w=2a%^m7)$6p3bfc7%hjv%^u^%sg-24l3^i3(v*95vr0)dc*^m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.simple_history",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "applications.apps.ApplicationsConfig",
    "bootstrap5",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cofas_2024.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'cofas_2024.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cofas',  #database name
        'USER': 'root',
        'PASSWORD': 'root', #ur db password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = 'media/'

# This should already be defined, just ensure it's correct
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')  # This line tells Django to also look for static files in the 'static' directory you created
]

# Collects static files into this directory when using 'python manage.py collectstatic'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = '8edb6f7b069c5f'
EMAIL_HOST_PASSWORD = '40577e6b2b9088'
EMAIL_PORT = '2525'
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "COFAS DASHBOARD",
    "SITE_HEADER": "COFAS DASHBOARD",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("/images/costechlogo1.svg"),
        "dark": lambda request: static("/images/costechlogo1.svg"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("/images/costechlogo1.svg"),
        "dark": lambda request: static("/images/costechlogo1.svg"),
    },
    "SITE_SYMBOL": "speed",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,

    "LOGIN": {
        "image": lambda request: static("sample/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },

    "COLORS": {
        "primary": {
            "50": "251 243 227",
            "100": "247 232 199",
            "200": "240 210 143",
            "300": "233 188 87",
            "400": "226 166 31",
            "500": "193 137 45",  # #c1892d
            "600": "154 110 36",
            "700": "116 82 27",
            "800": "77 55 18",
            "900": "39 27 9",
            "950": "19 14 4",
        },
    },

    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("COSTECH ADMIN"),
                "items": [
                    {
                        "title": _("Applications"),
                        "icon": "apps",
                        "link": reverse_lazy("admin:app_list", args=("applications",)),
                    },
                    {
                        "title": _("Settings"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:app_list", args=("auth",)),
                    },
                    {
                        "title": _("Analytics"),
                        "icon": "analytics",
                        "link": "#",
                    },
                ],
            },
        ],
    },
}