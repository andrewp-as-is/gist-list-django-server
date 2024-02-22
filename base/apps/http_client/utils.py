import http.client
from http.client import parse_headers
import io
import os
import time

from django.conf import settings
from base.settings import HTTP_CLIENT_DIR

http.client._MAXHEADERS = 1000


def get_timestamp():
    return round(time.time(), 3)


def get_disk_path(relpath):
    return os.path.join(HTTP_CLIENT_DIR, relpath)


def get_headers(value):
    if self.headers:
        if self.headers[0] == "{":  # json
            return json.loads(self.headers)
        else:  # plain text
            fp = io.BytesIO(self.headers.encode())
            return dict(parse_headers(fp)) if fp else {}
    return {}


def write_headers(path, data):
    text = "\n".join(map(lambda i: "%s: %s" % (i[0], i[1]), data.items()))
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    open(path, "w").write(text)
