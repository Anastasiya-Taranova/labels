from urllib.parse import urlsplit

from utils import get_setting


def get_db_host():
    url = get_setting("DATABASE_URL")
    if not url:
        raise RuntimeError("--- no database configured ---")

    url = urlsplit(url)
    host = url.hostname
    return host


def get_db_port():
    url = get_setting("DATABASE_URL")
    if not url:
        raise RuntimeError("--- no database configured ---")

    url = urlsplit(url)
    port = int(url.port or 5432)
    return port


def get_db_name():
    url = get_setting("DATABASE_URL")
    if not url:
        raise RuntimeError("--- no database configured ---")

    url = urlsplit(url)
    name = url.path.replace("/", "")
    return name


def get_db_username():
    url = get_setting("DATABASE_URL")
    if not url:
        raise RuntimeError("--- no database configured ---")

    url = urlsplit(url)
    return url.username
