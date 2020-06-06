from .base import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("POSTGRES_DB", "starnavi_db"),
        "USER": env.str("POSTGRES_USER", "starnavi_user"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", "starnavi_password"),
        "HOST": env.str("DB_HOST", "postgres"),
        "PORT": env.int("DB_PORT", 5432),
    }
}
