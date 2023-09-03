#!/usr/bin/env python
import json
import os
import requests

query="""
query {
  user(login: "andrewp-as-is") {
    followers(first: 100) {
      nodes {
        databaseId
        login
        email
        name
        bio
        company
        location
        websiteUrl
        gists {
          totalCount
        }
        followers {
          totalCount
        }
        following {
          totalCount
        }
        twitterUsername
        createdAt
        updatedAt
      }
      pageInfo {
        endCursor
      }
    }
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}

""".strip()
url = 'https://api.github.com/graphql'
# json = { 'query' : QUERY }
api_token = os.getenv("GITHUB_TOKEN")
headers = {
'Authorization': 'token %s' % api_token,
'Content-Type': 'application/json'
}

# r = requests.post(url=url, json=json, headers=headers)
data = """
{"query": "query {
  user(login: \\"andrewp-as-is\\") {\n    followers(first: 100) {\n      nodes {\n        databaseId\n        login\n        name\n        bio\n        company\n        location\n        websiteUrl\n        gists {\n          totalCount\n        }\n        followers {\n          totalCount\n        }\n        following {\n          totalCount\n        }\n        twitterUsername\n        createdAt\n        updatedAt\n      }\n      pageInfo {\n        endCursor\n      }\n    }\n  }\n  rateLimit {\n    limit\n    cost\n    remaining\n    resetAt\n  }\n}\n"}
"""
data =data.replace('\n',' ')
print(data)
r = requests.post(url=url, data=data, headers=headers)
print(r.status_code)
print (r.text)
