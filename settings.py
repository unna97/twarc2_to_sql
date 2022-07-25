from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbname',
        'USER': 'postgres',
        'PASSWORD': 'unnati',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
#django postgres setting 

INSTALLED_APPS = ('db',)

SECRET_KEY = 'REPLACE_ME'
