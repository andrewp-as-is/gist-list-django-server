#!/usr/bin/env python
import os
import requests


url = 'https://api.github.com/graphql'

headers = {
    "Authorization": "Bearer %s" % os.getenv('GITHUB_TOKEN'),
    'Accept':'application/vnd.github.v3.star+json'
}
query = """
{
   "query": "query {
     viewer {
       gist (name: \"5b10b34f87955dfc86d310cd623a61d1\" ) {
        stargazerCount
       }
     }
   }"
}
"""
r = requests.get(url,headers=headers,json={'query': query})
print(r)
print(r.text)
