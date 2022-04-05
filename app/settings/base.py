import os

from .path import TEMPLATES_PATH

DEBUG = bool(os.getenv('DEBUG'))
TEST = bool(os.getenv('TEST'))

ALLOWED_HOSTS = ['*']

DEFAULT_SECRET_KEY = 'secretsecret'
SECRET_KEY = os.getenv('SECRET_KEY', DEFAULT_SECRET_KEY)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    # 'api.middleware.CustomProcessException',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_PATH,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'garpix_menu.context_processors.menu_processor',
            ],
        },
    },
]

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

FILE_UPLOAD_PERMISSIONS = 0o644
AUTH_USER_MODEL = 'user.User'

LOGIN_REDIRECT_URL = '/'

SITE_ID = os.getenv('SITE_ID') or 1
SITE_URL = os.getenv('SITE_URL')
SITE_URL_FRONT = 'http://91.218.229.240:3001/'

DEFAULT_PAGE_SIZE = 9

PASSWORD_DURATION_DAYS = 90

RECAPTCHA_PRIVATE_KEY = 'get_key_from_google'
RECAPTCHA_PUBLIC_KEY = 'get_key_from_google'
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.5

CORS_ORIGIN_ALLOW_ALL = True

REDIS_PORT = os.getenv('POSTGRES_PORT', 6379)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
