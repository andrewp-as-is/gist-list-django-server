#!/usr/bin/env python
import os
import requests

# https://stackoverflow.com/questions/31199470/get-github-gist-stargazer-count
QUERY="""
# Type queries into this side of the screen, and you will
# see intelligent typeaheads aware of the current GraphQL type schema,
# live syntax, and validation errors highlighted within the text.

# We'll get you started with a simple query showing your username!
{
  viewer {
    gists (first: 100, privacy:ALL, orderBy: {field: CREATED_AT, direction: DESC} ) {
        nodes {
          description
          name
          isPublic
          isFork
          stargazerCount
          createdAt
          updatedAt
          pushedAt
          # files languages not available
            comments (first: 100) {
              totalCount
            }
            forks (first: 100) {
              totalCount
            }
            # todo: owner
            # history
        }
    }
  }
}




"""
url = 'https://api.github.com/graphql'
json = { 'query' : QUERY }
api_token = os.getenv("GITHUB_TOKEN")
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)

# print (r.text)
