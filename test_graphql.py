#!/usr/bin/env python
import os
import requests

url = 'https://api.github.com/graphql'
json = { 'query' : '{ viewer { repositories(first: 30) { totalCount pageInfo { hasNextPage endCursor } edges { node { name } } } } }' }
api_token = os.getenv("GITHUB_TOKEN")
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)

print (r.text)
print (dict(r.headers))
