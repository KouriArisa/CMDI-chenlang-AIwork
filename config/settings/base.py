import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")
MYSQL_PASSWORD_PLACEHOLDER = "change-this-password"


def get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name, str(default))
    return value.lower() in {"1", "true", "yes", "on"}


def get_list_env(name: str, default: str) -> list[str]:
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    raise ImproperlyConfigured(f"Missing required environment variable: {name}")


def get_mysql_password() -> str:
    password = get_required_env("MYSQL_PASSWORD")
    if password == MYSQL_PASSWORD_PLACEHOLDER:
        raise ImproperlyConfigured(
            "MYSQL_PASSWORD is still set to the example placeholder. "
            "Update it in .env before starting Django."
        )
    return password


SECRET_KEY = get_required_env("DJANGO_SECRET_KEY")
DEBUG = get_bool_env("DJANGO_DEBUG", True)
ALLOWED_HOSTS = get_list_env("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.todos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "config.middleware.ApiExceptionMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": get_required_env("MYSQL_DATABASE"),
        "USER": get_required_env("MYSQL_USER"),
        "PASSWORD": get_mysql_password(),
        "HOST": get_required_env("MYSQL_HOST"),
        "PORT": get_required_env("MYSQL_PORT"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
