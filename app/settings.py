import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Super-secret'
DEBUG = True

ALLOWED_HOSTS = []


PROJECT_APPS = (
    'app',
    'account',
    'corporative',
    'entrepreneur',
    'place',
)

INSTALLED_APPS = PROJECT_APPS + (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'django_countries',
    'widget_tweaks',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }


VALIDATOR = 'django.contrib.auth.password_validation.{0}'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': VALIDATOR.format('UserAttributeSimilarityValidator'),
    },
    {
        'NAME': VALIDATOR.format('MinimumLengthValidator'),
    },
    {
        'NAME': VALIDATOR.format('CommonPasswordValidator'),
    },
    {
        'NAME': VALIDATOR.format('NumericPasswordValidator'),
    },
]

AUTH_USER_MODEL = 'account.User'
LOGIN_URL = 'auth_login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_URL = 'user_logout'
LOGOUT_REDIRECT_URL = 'home'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

# Local settings
settings_file = __import__('app.local_settings').local_settings
for setting_value in dir(settings_file):
    locals()[setting_value] = getattr(settings_file, setting_value)
