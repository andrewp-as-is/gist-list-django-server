#!/usr/bin/env python
import requests


url = 'https://api.github.com/gists/starred'
# url = 'https://api.github.com/gists/kennethreitz/starred'

token='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'
print('url = %s' % url)
headers = {
    "Authorization": "Bearer %s" % token,
    'Accept':'application/vnd.github.v3.star+json'
}
r = requests.get(url,headers=headers)
print(r)
print(len(r.json()))
print(r.json())
