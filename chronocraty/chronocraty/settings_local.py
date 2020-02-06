

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER' : 'postgres',
        'PASSWORD' : 'postgres',
        # 'HOST' : '127.0.0.1',
        'HOST' : 'db',
        'PORT' : '5432',

    }
}

