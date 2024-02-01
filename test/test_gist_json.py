#!/usr/bin/env python
import requests

gist_id = '270c1953a62f62eeb2fb0414f9723321'
url = 'https://api.github.com/gists/%s' % gist_id
url = 'https://api.github.com/gists'
token='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'
print('url = %s' % url)
headers = {"Authorization": "Bearer %s" % token,'Accept':'application/vnd.github.v3.star+json'}
r = requests.get(url,headers=headers)
print(r.status_code)
print(r.headers['etag'])

# fork_of
