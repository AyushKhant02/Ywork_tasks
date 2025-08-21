INSTALLED_APPS = [
    
    'rest_framework',
    'channels',
    'employees',
    'chat'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',   # or MySQL/SQLite
        'NAME': 'companydb',
        'USER': 'youruser',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# WebSockets
ASGI_APPLICATION = "company.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    },
}

# MongoDB for chat
MONGO_DB = "chatdb"
MONGO_URI = "mongodb://localhost:27017/"
