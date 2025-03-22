"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from decouple import config, Csv, UndefinedValueError
import dj_database_url
from django.core.exceptions import ImproperlyConfigured  # Add this line

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Determine environment
IS_VERCEL = bool(os.environ.get('VERCEL', False))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = config('DJANGO_SECRET_KEY')
except UndefinedValueError:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY environment variable is required")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

# Get allowed hosts from environment variable or use defaults
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker',
    'tracker.templatetags',
    'django_ratelimit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django_permissions_policy.PermissionsPolicyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'errors'),  # Add error templates
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Database configuration for both local and Vercel
if os.environ.get('VERCEL'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',  # Using Vercel's writable /tmp directory
            'OPTIONS': {
                # Disable deterministic to support older SQLite versions
                'deterministic': False,
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                # Keep deterministic True for local development
                'deterministic': True,
            }
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Static files configuration
STATIC_URL = 'static/'

if os.environ.get('VERCEL'):
    STATIC_ROOT = '/tmp/static'
    STATICFILES_DIRS = []  # Empty for Vercel
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Changed from 'static'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]

# Ensure WhiteNoise is properly configured
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = 31536000  # 1 year

# Create static directory if it doesn't exist (local development only)
if not os.environ.get('VERCEL'):
    os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs and redirects
LOGIN_URL = 'login'  # Remove leading slash
LOGIN_REDIRECT_URL = 'supplement_record'  # Use URL name instead of path
LOGOUT_REDIRECT_URL = 'choose_mode'  # Use URL name instead of path

# Security settings - Make them conditional based on environment
if not DEBUG:  # Only enable these settings in production
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_DOMAIN = None  # Restrict to same origin
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_NAME = '__Secure-csrftoken'  # Only when using HTTPS
    CSRF_COOKIE_SAMESITE = 'Lax'
    CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 24  # 24 hours
    USE_ETAGS = True

    # Verify critical production settings
    required_settings = {
        'DJANGO_SECRET_KEY': os.environ.get('DJANGO_SECRET_KEY'),
        'ALLOWED_HOSTS': os.environ.get('ALLOWED_HOSTS'),
    }

    missing_settings = [k for k, v in required_settings.items() if not v]
    if missing_settings:
        raise ImproperlyConfigured(
            f"Missing required production settings: {', '.join(missing_settings)}"
        )
else:  # Development settings
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False


"""
Security Headers Configuration
----------------------------
- XSS Filter: Enabled
- Content Type Options: No-sniff
- X-Frame-Options: DENY
- Referrer Policy: Same-origin
- HSTS: Enabled in production
"""
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Additional security headers
SECURE_REFERRER_POLICY = 'same-origin'
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # Allow inline styles
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'")  # For development
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "https:", "data:")

# Add session security settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = '__Secure-sessionid' if not DEBUG else 'sessionid'

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

# Minimal logging configuration
LOGGING_CONFIG = None
LOGGING = None

# Replace the basic logging configuration
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',  # Fixed: changed levellevel to levelname
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Base Logging Configuration
if IS_VERCEL:
    # Vercel: Console-only logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '[%(asctime)s] %(levelname)s: %(message)s',  # Fixed: changed levellevel to levelname
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            }
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            }
        }
    }
else:
    # Local: Console and file logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '[%(asctime)s] %(levelname)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'django.log'),
                'maxBytes': 1024*1024*5,  # 5 MB
                'backupCount': 5,
                'formatter': 'simple',
            }
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console', 'file'],
                'level': 'WARNING',
                'propagate': False,
            }
        }
    }

# Add request logging for security monitoring
LOGGING['loggers']['django.request'] = {
    'handlers': ['console', 'file'],
    'level': 'WARNING',
    'propagate': True,
}

# Cache Configuration
# Update cache settings based on environment
if os.environ.get('VERCEL'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

# Update rate limiting settings
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_FAIL_OPEN = False

# Ignore rate limit warnings in development
if DEBUG:
    import logging
    logging.getLogger('django_ratelimit').setLevel(logging.ERROR)

PERMISSIONS_POLICY = {
    'geolocation': 'none',
    'camera': 'none',
    'microphone': 'none',
}

def validate_env_vars():
    """Validate critical environment variables on startup."""
    required_vars = {
        'DJANGO_SECRET_KEY': 'Required for security',
        'ALLOWED_HOSTS': 'Required in production',
    }

    if not DEBUG:
        missing = [var for var, msg in required_vars.items()
            if not config(var, default=None)]
        if missing:
            raise ImproperlyConfigured(
                f"Missing required environment variables: {', '.join(missing)}"
            )

# Call at the end of settings.py
validate_env_vars()

# Error handling configuration
handler404 = 'tracker.views.custom_404'
handler500 = 'tracker.views.custom_500'
handler403 = 'tracker.views.custom_403'