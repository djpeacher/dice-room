import dj_database_url
from .common import *

ADMIN_URL = os.environ['ADMIN_URL']
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(",")
DATABASES = {"default": dj_database_url.config()}
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
