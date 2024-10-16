"""
Django settings for open_class_diagrammer project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import json
from django.urls import reverse_lazy

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
SECRET_KEY_FALLBACKS = json.loads(os.environ.get('SECRET_KEY_FALLBACKS', '[]'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("ENV", "PROD") == "DEV"

ALLOWED_HOSTS = ["127.0.0.1:8000", "localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    "class_manager",
    "tailwind",
    "theme",
    "django_browser_reload"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware"
]

ROOT_URLCONF = 'open_class_diagrammer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'open_class_diagrammer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if 'JAWSDB_URL' in os.environ:
    import re

    jawsdb_url = os.environ['JAWSDB_URL']
    match = re.match(
        r'mysql:\/\/(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:/]+):(?P<port>\d+)/(?P<database>.+)',
        jawsdb_url,
    )

    if match:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': match.group('database'),
                'USER': match.group('user'),
                'PASSWORD': match.group('password'),
                'HOST': match.group('host'),
                'PORT': match.group('port'),
                'OPTIONS': {
                    'charset': 'utf8mb4',
                },
            }
        }
else:
    # Use custom settings for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('SCHEMA'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_URL'),
            'PORT': os.environ.get('DB_PORT')
        }
    }

# Authentication

LOGIN_URL = reverse_lazy("login")

LOGIN_REDIRECT_URL = reverse_lazy("class_manager:projects")

LOGOUT_REDIRECT_URL = reverse_lazy("home")

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = f"{BASE_DIR}/static"

STATICFILES_DIRS = [
    "class_manager/static",
    "theme/static"
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Tailwind Settings

TAILWIND_APP_NAME = "theme"

INTERNAL_IPS = ["127.0.0.1"]