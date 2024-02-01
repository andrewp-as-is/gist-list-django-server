from ..utils import get_stat_data

def get_most_used_tag_list(user_stat,secret):
    text_stat = user_stat.public_tag_stat
    if secret:
        text_stat = user_stat.secret_tag_stat
    data = get_stat_data(text_stat)
    sorted_dict = {r: data[r] for r in sorted(data, key=data.get, reverse=True)}
    return list(sorted_dict.keys())[0:5]

def get_top_language_list(user_stat,secret):
    text_stat = user_stat.public_language_stat
    if secret:
        text_stat = user_stat.secret_language_stat
    print('text_stat: %s' % text_stat)
    data = get_stat_data(text_stat)
    sorted_dict = {r: data[r] for r in sorted(data, key=data.get, reverse=True)}
    return list(sorted_dict.keys())[0:5]
