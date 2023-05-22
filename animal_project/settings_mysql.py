"""
Django settings for animal_project project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

import errno
import environ
env = environ.Env()
env.read_env('.env')

HEROKU_ENV = env.bool('DJANGO_HEROKU_ENV', default=False)

if not HEROKU_ENV:
    env.read_env('.env')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'accounts.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'adopt_animals',
    'phone_field',
    'social_django', 
    'cloudinary_storage',
    'cloudinary',
    'django_cleanup.apps.CleanupConfig',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'social_django.middleware.SocialAuthExceptionMiddleware', 
]

ROOT_URLCONF = 'animal_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends', 
                'social_django.context_processors.login_redirect', 
            ],
        },
    },
]

WSGI_APPLICATION = 'animal_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'heroku_289c99319ec0957',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }, 
        'USER': 'b8e7f890b8028a',
        'PASSWORD': 'e6813d0a',
        'HOST': 'us-cdbr-east-04.cleardb.com',
        'PORT': 3306
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'


LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login' 


SECRET_KEY=env("SECRET_KEY")
EMAIL=env("EMAIL")
PASSWORD=env("PASSWORD")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'testoma1212@gmail.com'
EMAIL_HOST_PASSWORD = 'gkqcxweapsekkojn'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    # 'social_core.backends.google.GoogleOpenId',
    # 'social_core.backends.google.GoogleOAuth2',

    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '453129612673-p12fi4v233oi2o8nndsneek062st7lth.apps.googleusercontent.com'  
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'ycXM_SLQeYHZZVOxeW2YcBS4' 

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dl2blqao5',
    'API_KEY': '813939149428973',
    'API_SECRET': 'lvXOZK0nJpwNC7_VmqV-dyd1T64'
}

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = EMAIL
EMAIL_HOST_PASSWORD = PASSWORD

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'