from decouple import config

from .base import *  # noqa: F401, F403

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("PGDATABASE", default="nicia_track"),
        "USER": config("PGUSER", default="nicia"),
        "PASSWORD": config("PGPASSWORD", default=""),
        "HOST": config("PGHOST", default="localhost"),
        "PORT": config("PGPORT", default="5432"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {"sslmode": config("DB_SSLMODE", default="require")},
    }
}

# Atrás do proxy reverso do Render, o Django só sabe que a requisição
# original era HTTPS pelo header X-Forwarded-Proto. Sem isto,
# SECURE_SSL_REDIRECT entra em loop infinito de redirecionamento.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Desativado temporariamente para validação de deploy via HTTP.
# Reativar quando Nginx + HTTPS estiverem configurados (Fase 4).
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Django 4.x exige origins confiáveis para aceitar POST sob HTTPS.
# Sem isto, todos os formulários falham com 403 CSRF em produção.
# Ex.: CSRF_TRUSTED_ORIGINS=https://nicia-track.onrender.com
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config("CSRF_TRUSTED_ORIGINS", default="").split(",")
    if origin.strip()
]

# Logs de WARNING+ para stdout/stderr — capturados pelo Render automaticamente.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
