import re

def get_hashtag_list(description):
    return list(map(lambda s:s.replace('#',''),sorted(map(
        lambda s:s,
        re.findall(r'\B#\w*[a-zA-Z]+\w*', description or '')
    ))))
