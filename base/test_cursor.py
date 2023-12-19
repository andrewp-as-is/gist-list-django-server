import re

query = """
query {
  viewer {
    gists (first: 100, privacy:ALL, after: null, orderBy: {field: CREATED_AT, direction: DESC}) {
        nodes {
          description
        }
    }
}
"""
REGEX = re.compile('after:(\")?(.*)(\")?,')

def replace_cursor(query,cursor):
    line_list = query.strip().splitlines()
    line_list[2] = REGEX.sub('after:"%s",' % cursor, line_list[2])
    return "\n".join(line_list)

cursor = "CURSOR!1111"
print(query)
query = replace_cursor(query,cursor)
print(query)
