"""
Django settings for animal_project project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# ファイルの存在チェック用モジュール
import errno
# environをインポートして読み込む
import environ
env = environ.Env()
env.read_env('.env')

# herokuの環境かどうか
HEROKU_ENV = env.bool('DJANGO_HEROKU_ENV', default=False)

# herokuの環境でない時は.envファイルを読む
if not HEROKU_ENV:
    env.read_env('.env')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

DEBUG=env.bool('DEBUG', False)

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'accounts.User'


# Application definition

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
    # 投稿に紐付けされている写真を削除
    'django_cleanup.apps.CleanupConfig',
    # |add_class:"form-control"を使用できるようにする
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

    'whitenoise.middleware.WhiteNoiseMiddleware',
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

                'social_django.context_processors.backends',  # これを追加
                'social_django.context_processors.login_redirect', # これを追加
            ],
        },
    },
]

WSGI_APPLICATION = 'animal_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'heroku_289c99319ec0957',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        'USER': 'b8e7f890b8028a',
        'PASSWORD': 'e6813d0a',
        'HOST': 'us-cdbr-east-04.cleardb.com',
        'PORT': 3306
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = '/' # ログイン後のデフォルト遷移ページ
LOGOUT_REDIRECT_URL = '/accounts/login' # ログアウトした時のログインページへのリダイレクト先

# manage.pyと同じ階層に.envファイルを作り、そちらへ
# 必要な情報は格納する。そして下記のように呼び出す。
# SECURITY WARNING: keep the secret key used in production secret!
DEBUG=env.bool('DEBUG', False)
SECRET_KEY=env("SECRET_KEY")
EMAIL=env("EMAIL")
PASSWORD=env("PASSWORD")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Email setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'testoma1212@gmail.com'
EMAIL_HOST_PASSWORD = 'gkqcxweapsekkojn'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',

    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

# Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '453129612673-p12fi4v233oi2o8nndsneek062st7lth.apps.googleusercontent.com'  # クライアントID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'ycXM_SLQeYHZZVOxeW2YcBS4' # クライアント シークレット

# Facebook
# SOCIAL_AUTH_FACEBOOK_KEY = '1579134558950637' 
# SOCIAL_AUTH_FACEBOOK_SECRET = 'a2f785f216164a5c73b26830190cb0a5'  

# Twitter
# SOCIAL_AUTH_TWITTER_KEY = 'PxtrK2mNfK3kFdFioJg27U2LK'
# SOCIAL_AUTH_TWITTER_SECRET = 'JAQloWLxYtoAfpTlUXd8MOorT7wVx5Fv9TfB74iSGWPvLXovbR'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dl2blqao5',
    'API_KEY': '813939149428973',
    'API_SECRET': 'lvXOZK0nJpwNC7_VmqV-dyd1T64'
}

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Email setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = EMAIL
EMAIL_HOST_PASSWORD = PASSWORD

# アイコンやロゴ表示用
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'