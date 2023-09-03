#!/usr/bin/env python
import os
import requests

# https://stackoverflow.com/questions/31199470/get-github-gist-stargazer-count
QUERY="""

"""
url = 'https://api.github.com/graphql'
json = { 'query' : QUERY }
api_token = os.getenv("GITHUB_TOKEN")
headers = {'Authorization': 'token %s' % api_token}

r = requests.head(url=url, headers=headers)
print (r.status_code)
print (r.headers)
print (r.text)
