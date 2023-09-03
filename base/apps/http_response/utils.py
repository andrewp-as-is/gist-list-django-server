import http.client
from http.client import parse_headers
import io
import os
import time
from urllib.parse import parse_qs, urlparse

from base.conf import ROOT_DIRNAME

http.client._MAXHEADERS = 42


def get_headers(text):
    fp = io.BytesIO(text)
    return dict(parse_headers(fp)) if fp else {}


def get_path(relpath):
    if relpath:
        return os.path.join(ROOT_DIRNAME,'response',relpath)

def get_timestamp():
    return int(time.time())
