#!/usr/bin/env python
import json
import os

import requests


url = 'https://api.github.com/gists'
# url = 'https://api.github.com/gists/kennethreitz/starred'

token=os.getenv('GITHUB_TOKEN')
files = {}
for i, name in enumerate(['test_NEW.txt']):
    files[name] = dict(content='content', filename=name)
url = "https://api.github.com/gists"
headers = {
    "Authorization": "Bearer %s" % token,
    "X-GitHub-Api-Version": "2022-11-28"
}
data = dict(public=False, description='description', files=files)
r = requests.post(url, headers=headers, data=json.dumps(data),timeout=5)
print(r.status_code)
print(r.text)

# 'created_at': '2020-05-20T16:45:31Z', 'updated_at': '2020-05-24T14:26:17Z'
# 'created_at': '2020-05-20T16:45:31Z', 'updated_at': '2020-05-24T14:26:17Z'}
