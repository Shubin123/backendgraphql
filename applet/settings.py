"""
Django settings for applet project.

Generated by 'django-admin startproject' using Django
"""

from pathlib import Path
from telnetlib import AUTHENTICATION
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["authoreteh.herokuapp.com", "127.0.0.1", "127.0.0.1:8000",
                 "127.0.0.1:8000/graphql", ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    "graphene_django",
    "applet.modelstore",
    "graphql_auth",
    'django_filters',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',

]

AUTH_USER_MODEL = "modelstore.User"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = False
# corsvar = os.getenv('frontendwhitelist', 'http://127.0.0.1:9000')


CORS_ORIGIN_WHITELIST = [
    os.getenv('frontendfilename', 'http://127.0.0.1:9000')
    # production url saved on heroku as cors header validation
]

ROOT_URLCONF = 'applet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'applet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': str(BASE_DIR / 'db.sqlite3'),
#     }
# }

# database first argument calls heroku enviroment variables second defaults
# to testing database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('dbname', 'postgres'),
        'USER': os.getenv('iiofwxsmjhzxye', 'postgres'),
        'PASSWORD': os.getenv('dbpassword', 'y2x^p)szf$j^le)59yh#i22y(''9#h6j#__)z+eqscmg(5w-uz2$'),
        'HOST': os.getenv('dbhost', 'localhost'),
        'PORT': os.getenv('dbport', 10000)
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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



GRAPHENE = {
    "SCHEMA": "applet.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware",
                   'corsheaders.middleware.CorsMiddleware'],
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
    "graphql_auth.backends.GraphQLAuthBackend",
]

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    # optional
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    # "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7),
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifyToken",
    ],
}

GRAPHQL_AUTH = {
        'LOGIN_ALLOWED_FIELDS': ['email', 'username'],
        'SEND_ACTIVATION_EMAIL': True,
    }



# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.titan.email"
EMAIL_PORT = "587"
DEFAULT_FROM_EMAIL = "me@shubin.email"
EMAIL_HOST_USER = "me@shubin.email"
EMAIL_HOST_PASSWORD = "R&b#H2h2yRm^%Tw"


SECRET_KEY = os.getenv('SECRET_KEY', 'Optional default value')


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
