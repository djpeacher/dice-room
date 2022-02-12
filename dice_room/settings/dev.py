from dotenv import load_dotenv
load_dotenv()
from .common import *

ADMIN_URL = 'admin/'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DEBUG = True
SECRET_KEY = 'django-insecure-#45wyo#)vk^r5&$!68qz5jinmj+bhgx-!792f)+j=#*qksc4+2'
