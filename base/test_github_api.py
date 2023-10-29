#!/usr/bin/env python
import os
import requests

url = "https://api.github.com/"
api_token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": "token %s" % "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"}

r = requests.head(url=url, headers=headers)
print(r.status_code)
print(r.headers)
print(r.text)
