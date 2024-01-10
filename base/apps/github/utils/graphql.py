from urllib.parse import parse_qs, urlparse

# todo: sort order. wut with etag?

def get_user_followers_query(login,after=None):
    return """
query {
  user(login: \"%s\") {
    followers(first: 100, after: %s) {
      nodes {
        databaseId
        login
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
        startCursor
        endCursor
        hasNextPage
        hasPreviousPage
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
""" % (login,'"%s"' % after if after else 'null')

def get_user_following_query(login,after=None):
    return """
query {
  user(login: \"%s\") {
    following(first: 100,after: %s) {
      nodes {
        databaseId
        login
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
        startCursor
        endCursor
        hasNextPage
        hasPreviousPage
      }
    }
  }
}
""" % (login,'"%s"' % after if after else 'null')

def get_user_gists_query(login,after=None):
    return """
query {
  user(login: \"%s\") {
    gists (first: 100, after: %s, orderBy: {field: CREATED_AT, direction: DESC}) {
        nodes {
          description
          name
          isPublic
          isFork
          stargazerCount
          createdAt
          updatedAt
          pushedAt
          comments (first: 100) {
            totalCount
          }
          forks (first: 100) {
            totalCount
          }
        }
      pageInfo {
        startCursor
        endCursor
        hasNextPage
        hasPreviousPage
      }
    }
  }
}
""" % (login,'"%s"' % after if after else 'null')\

def get_viewer_gists_query(after=None):
    return """
query {
  viewer {
    gists (first: 100, privacy:ALL, after: %s, orderBy: {field: CREATED_AT, direction: DESC}) {
        nodes {
          description
          name
          isPublic
          isFork
          stargazerCount
          createdAt
          updatedAt
          pushedAt
          comments (first: 100) {
            totalCount
          }
          files {
            name
          }
          forks (first: 100) {
            totalCount
          }
        }
        pageInfo {
          startCursor
          endCursor
          hasNextPage
          hasPreviousPage
        }
    }
  }
}
""" % ('"%s"' % after if after else 'null')

def get_login(url):
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)["login"][0]

def get_query(url,after=None):
    if 'user.followers' in url:
        return get_user_followers_query(get_login(url),after)
    if 'user.following' in url:
        return get_user_following_query(get_login(url),after)
    if 'user.gists' in url:
        return get_user_gists_query(get_login(url),after)
    if 'viewer.gists' in url:
        return get_viewer_gists_query(get_login(url),after)
