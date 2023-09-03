#!/usr/bin/env python
import requests


url = 'https://api.github.com/users/hofmannsven/gists'

token='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'
print('url = %s' % url)
headers = {"Authorization": "Bearer %s" % token,'Accept':'application/vnd.github.v3.star+json'}
r = requests.get(url,headers=headers)
print(r.status_code)
print(r.json())

# 'created_at': '2020-05-20T16:45:31Z', 'updated_at': '2020-05-24T14:26:17Z'
# 'created_at': '2020-05-20T16:45:31Z', 'updated_at': '2020-05-24T14:26:17Z'}
