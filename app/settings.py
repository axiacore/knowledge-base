import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '05se#blzw_s^8cb7^2_c56o&88=jf&fawfm9$t!7@)t7fwp&sp'

DEBUG = True

ALLOWED_HOSTS = []

PROJECT_APPS = [
    'app',
]

INSTALLED_APPS = PROJECT_APPS + [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'axes',
    'compressor',
    'django_extensions',
    'django_jenkins',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # TypeError: object.__init__() takes no parameters
    # 'axes.middleware.FailedLoginMiddleware',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/uploads/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')


# django-axes
AXES_LOGIN_FAILURE_LIMIT = 3
AXES_USE_USER_AGENT = True
AXES_COOLOFF_TIME = 24
AXES_LOCKOUT_TEMPLATE = '429.html'

# django-compressor
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]
