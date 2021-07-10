"""
Django settings for yechimlar project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from environs import Env
from corsheaders.defaults import default_headers


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "mm*jsis%wp4uv^p#-efb5cz^1*kmkt89w)yy^p6x3_&99jd2%x"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# ALLOWED_HOSTS = ['176.99.11.80', 'localhost', '127.0.0.1', ]
# CORS_ALLOWED_ORIGINS = '*'
# CORS_ALLOWED_ORIGINS = [
#     'http://brainly.uz',
#     'http://176.99.11.80:3333',
# 'http://176.99.11.80:8050',
#     'http://localhost:8000',
#
# ]
# CSRF_TRUSTED_ORIGINS = [
#     'http://brainly.uz',
# ]
# CORS_ALLOW_ALL_ORIGINS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'main',
    'django_filters',
    'django_rest_passwordreset',
    # 'drf-composable-permissions',
    'rest_condition',
    # 'corsheaders',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bilim.urls'


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

WSGI_APPLICATION = 'bilim.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mirjahonn.mysql.pythonanywhere-services.com',
        'NAME': 'programmerDX$default',
        'USER': 'mirjahonn',
        'PASSWORD': "(']$fcrX\]D'23j-"}
}

# import dj_database_url
#
# DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
# DATABASES['default'] = dj_database_url.config(default='postgres://ecxcygtpdciufq:7fd3f1ac4696c304059c6fc498590f64cdf65e67443a153a60ac0cd3f4e11b0c@ec2-54-91-188-254.compute-1.amazonaws.com:5432/ddpp380imdt5qg')


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Password Reset
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 'static' is my media folder


MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')  # 'media' is my media folder
MEDIA_URL = 'https://programmerDX.pythonanywhere.com/media/'  # production
# MEDIA_URL = 'http://127.0.0.1:8000/media/'   # development

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


APPEND_SLASH = False

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'bilim.pagination.CustomPagination',
    'PAGE_SIZE': 15,
}
