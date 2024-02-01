#!/usr/bin/env python
import requests


url = 'https://api.github.com/gists/8475c387fe49d5e04b095ef98c885518'
url = 'https://api.github.com/gists/starred'

token='' # gists42.com localhost
#token='' # $GITHUB_TOKEN
print('url = %s' % url)
headers = {"Authorization": "Bearer %s" % token,'Accept':'application/vnd.github.v3+json'}
r = requests.get(url,headers=headers)
print(r)
print(r.text)
