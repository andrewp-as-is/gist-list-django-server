
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
        endCursor
      }
    }
  }
}
""" % (login,'"%s"' % after if after else 'null')

def get_user_gists_query(login,after=None):
    return """
query {
  user(login: \"%s\") {
    gists (first: 100, after: %s, orderBy: {field: CREATED_AT, direction: DESC} ) {
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
        endCursor
      }
    }
  }
}
""" % (login,'"%s"' % after if after else 'null')\

def get_viewer_gists_query(after=None):
    return """
query {
  viewer {
    gists (first: 100, privacy:ALL, after: %s, orderBy: {field: CREATED_AT, direction: DESC} ) {
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
          endCursor
        }
    }
  }
}
""" % ('"%s"' % after if after else 'null')
