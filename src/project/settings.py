from pathlib import Path

import dj_database_url
import sentry_sdk
from django.urls import reverse_lazy
from dynaconf import settings as _settings
from sentry_sdk.integrations.django import DjangoIntegration

from scripts.dirs import DIR_PROJECT, DIR_REPO
from scripts.utils import get_setting

SECRET_KEY = _settings.SECRET_KEY

DEBUG = _settings.DEBUG

ALLOWED_HOSTS = _settings.ALLOWED_HOSTS + ["localhost", "127.0.0.1"]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

INSTALLED_APPS_ORDERED = {
    0: "django.contrib.admin",
    10: "django.contrib.auth",
    20: "django.contrib.contenttypes",
    30: "django.contrib.sessions",
    40: "django.contrib.messages",
    50: "django.contrib.staticfiles",
    60: "django.contrib.sites",
    2000: "allauth",
    3000: "allauth.account",
    4000: "allauth.socialaccount",
    5000: "allauth.socialaccount.providers.github",
    1000: "applications.index.apps.IndexConfig",
}

INSTALLED_APPS = [app for _, app in sorted(INSTALLED_APPS_ORDERED.items())]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            DIR_PROJECT / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

_db_url = _settings.DATABASE_URL

if _settings.ENV_FOR_DYNACONF == "heroku":
    _db_url = get_setting("DATABASE_URL")

DATABASES = {"default": dj_database_url.parse(_db_url, conn_max_age=600)}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = _settings.SITE_ID

STATIC_URL = "/assets/"

STATICFILES_DIRS = [DIR_PROJECT / "static"]

STATIC_ROOT = DIR_REPO / ".static"

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "APP": {
            "client_id": _settings.GITHUB_CLIENT_ID,
            "secret": _settings.GITHUB_SECRET,
        },
        "SCOPE": [
            "user",
            "repo",
            "admin:org",
        ],
    }
}

sentry_sdk.init(
    get_setting("SENTRY_DSN"),
    traces_sample_rate=1.0,
)

ACCOUNT_EMAIL_VERIFICATION = "none"

LOGIN_REDIRECT_URL = reverse_lazy("index:index")
