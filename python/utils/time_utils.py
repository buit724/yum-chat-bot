from datetime import datetime
from zoneinfo import ZoneInfo

DATE_TIME_FMT = "%m/%d/%Y, %I:%M:%S%p %Z"
TIME_FMT = "%H:%M:%S"
CHANNEL_TZ = ZoneInfo("America/New_York")


def current_time() -> datetime:
    return datetime.now().astimezone(CHANNEL_TZ)


def format_datetime_tz_aware(time: datetime) -> str:
    return time.strftime(DATE_TIME_FMT)


def format_datetime_tz_unaware(time: datetime) -> str:
    return format_datetime_tz_aware(time.astimezone(CHANNEL_TZ))


def format_time_24h(time: datetime) -> str:
    return time.strftime(TIME_FMT)
