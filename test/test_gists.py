#!/usr/bin/env python
import requests


url = 'https://api.github.com/gists'
# url = 'https://api.github.com/gists/kennethreitz/starred'

token='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'
print('url = %s' % url)
headers = {"Authorization": "Bearer %s" % token,'Accept':'application/vnd.github.v3.star+json'}
r = requests.get(url,headers=headers)
print(r.status_code)
print(r.headers['etag'])

# 'created_at': '2020-05-20T16:45:31Z', 'updated_at': '2020-05-24T14:26:17Z'
# 'created_at': '2020-05-20T16:45:31Z', 'updated_at': '2020-05-24T14:26:17Z'}
