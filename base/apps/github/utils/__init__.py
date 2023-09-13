from datetime import datetime
import time
import pytz

def get_api_timestamp(string):
    if not string:
        return
    d = datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")
    return int(pytz.timezone('UTC').localize(d).timestamp())
