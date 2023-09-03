from datetime import datetime

def get_api_timestamp(string):
    if not string:
        return
    return int(datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ").timestamp())
