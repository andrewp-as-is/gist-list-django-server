#!/usr/bin/env python
import requests


url = 'https://api.github.com/gists/85813f11a0038867a449f1624c3a7810/stargazers'
# url = 'https://api.github.com/gists/kennethreitz/starred'

token='' # gists42.com localhost
print('url = %s' % url)
headers = {"Authorization": "Bearer %s" % token,'Accept':'application/vnd.github.v3.star+json'}
r = requests.get(url,headers=headers)
print(r.json())
