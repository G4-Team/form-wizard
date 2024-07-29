from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

SECRET_KEY = env("PRODUCTION_SECRET_KEY")

DATABASES = {
    "default": env.db("DATABASE_URL")
}