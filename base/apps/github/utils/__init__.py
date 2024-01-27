from datetime import datetime
import time
import pytz

def get_api_timestamp(string):
    if not string:
        return
    d = datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")
    return int(pytz.timezone('UTC').localize(d).timestamp())


def get_raw_path(gist,filename):
    # user_id/gist_id/filename
    return 'todo'
