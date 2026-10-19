import os
from pathlib import Path
from dotenv import load_dotenv

# BASE_DIR ni aniqlash
BASE_DIR = Path(__file__).resolve().parent.parent

# .env faylini yuklash
load_dotenv(os.path.join(BASE_DIR, '.env'))

# MAXFIY KALIT VA DEBUG SOZLAMALARI
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-it-shaharcha-toshloq-fergana-secret-key-2026')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# ULANAN ILOVALAR (INSTALLED APPS)
INSTALLED_APPS = [
    # Django standart ilovalari
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Bizning loyiha ilovalari
    'accounts',
    'courses',
    'applications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# SHABLONLAR (TEMPLATES) SOZLAMALARI
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # templates papkasi ulangan
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

WSGI_APPLICATION = 'core.wsgi.application'


# MA'LUMOTLAR BAZASI (SQLite -> keyinchalik PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# PAROL XAVFSIZLIGI SINOVLARI
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


# MAXSUS FOYDALANUVCHI MODELI
AUTH_USER_MODEL = 'accounts.CustomUser'


# TILI VA VAQT MINTAQASI (O'zbekiston, Toshkent vaqti)
LANGUAGE_CODE = 'uz-uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# STATIK VA MEDIA FAYLLAR SOZLAMALARI
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# DEFAULT AUTO FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# LOGIN VA LOGOUT YO'NALISHLARI
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'


# TELEGRAM BOT INTEGRATSIYASI (.env faylidan olinadi)
TELEGRAM_BOT_TOKEN = '8373580640:AAHJFoAyUM6qNjI_o_nqFDtIFPa03WW4bXw'
TELEGRAM_CHAT_ID = '8328359338'
# Telegram Bot settings
TELEGRAM_BOT_TOKEN = '8373580640:AAHJFoAyUM6qNjI_o_nqFDtIFPa03WW4bXw'
TELEGRAM_CHAT_ID = '8328359338'