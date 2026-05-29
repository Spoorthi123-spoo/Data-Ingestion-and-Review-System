from pathlib import Path
from datetime import timedelta

# -----------------------------------
# BASE DIRECTORY
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------
# SECURITY
# -----------------------------------
SECRET_KEY = 'django-insecure-change-this-in-production'

DEBUG = True

ALLOWED_HOSTS = ["*"]   # ✅ FIXED HERE

# -----------------------------------
# INSTALLED APPS
# -----------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REST FRAMEWORK
    'rest_framework',
    'django_filters',

    # CORS
    'corsheaders',

    # ESG APPS
    'esg_ingestion',
    'normalization',
    'reviews',
    'audit',
    'emissions',
]

# -----------------------------------
# MIDDLEWARE
# -----------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ ADDED

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------------
# URL CONFIG
# -----------------------------------
ROOT_URLCONF = 'backend.urls'

# -----------------------------------
# TEMPLATES
# -----------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -----------------------------------
# WSGI
# -----------------------------------
WSGI_APPLICATION = 'backend.wsgi.application'

# -----------------------------------
# DATABASE
# -----------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------------
# PASSWORD VALIDATION
# -----------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------------
# INTERNATIONALIZATION
# -----------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------------------
# STATIC FILES
# -----------------------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"   # ✅ FIXED

# -----------------------------------
# DEFAULT PRIMARY KEY
# -----------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------
# CORS
# -----------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# -----------------------------------
# DRF + JWT
# -----------------------------------
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# -----------------------------------
# SIMPLE JWT CONFIG
# -----------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}