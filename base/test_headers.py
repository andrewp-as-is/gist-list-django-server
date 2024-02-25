#!/usr/bin/env python
import os
import requests

url = "https://api.github.com/"
r = requests.head(url=url)
for k,v in r.headers.items():
    print('%s: %s' % (k,v))
