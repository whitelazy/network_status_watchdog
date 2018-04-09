from datetime import datetime

default_tz = None


def set_default_timezone(tz):
    global default_tz
    default_tz = tz


def get_datetime_string(tz=None):
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"

    global default_tz

    if tz:
        return datetime.now(tz).strftime(fmt)
    else:
        if default_tz:
            return datetime.now(default_tz).strftime(fmt)
        else:
            return datetime.now().strftime(fmt)
