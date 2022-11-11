import datetime as dt
import pytz
from config import SYS_PREFS

TIMEZONE=pytz.timezone(SYS_PREFS['TIMEZONE'])

def timestamp_to_tz_aware(timestamp:int)->dt.datetime:
    return dt.datetime.fromtimestamp(timestamp, tz=TIMEZONE)

def add_minutes_to_time(time:dt.datetime, minutes:int)->dt.datetime:
    return time + dt.timedelta(minutes=minutes)

def get_aware_now()->dt.datetime:
    return dt.datetime.now(tz=TIMEZONE)

def round_minutes_down(time:dt.datetime, minutes_to_round)->dt.datetime:
    time = time.replace(second=0, microsecond=0)
    minus = time.minute % minutes_to_round
    return time.replace(minute=time.minute - minus)