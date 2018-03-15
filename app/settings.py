import os
from django.utils.translation import ugettext_lazy as _

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
    'social_django',
    'widget_tweaks',
    'storages',
    'huey.contrib.djhuey',
)

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

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'app.context_processors.facebook_app_id',
                'app.context_processors.permissions',
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
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_URL = 'user_logout'
LOGOUT_REDIRECT_URL = 'home'


AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'first_name, last_name, email',
}
SOCIAL_AUTH_USER_FIELDS = [
    'first_name',
    'last_name',
    'email',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'level-and-date': {
            'format':
            '%(levelname)s\t%(asctime)s\t%(funcName)s\t%(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'level-and-date',
        },
    },
    'loggers': {
        'huey': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

BASE_URL = 'https://queryjane.net'

EMAIL_SUBJECT = 'QueryJane - {0}'
ADMIN_EMAILS = []

SOCIAL_AUTH_FACEBOOK_KEY = 'edit-it'
SOCIAL_AUTH_FACEBOOK_SECRET = 'edit-it'

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Local settings
settings_file = __import__('app.local_settings').local_settings
for setting_value in dir(settings_file):
    locals()[setting_value] = getattr(settings_file, setting_value)
