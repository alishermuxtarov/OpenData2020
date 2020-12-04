from config.settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

print("\n\n\t[USED TEST SETTINGS]\n\n")
