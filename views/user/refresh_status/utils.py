
def get_user_id(url):
    return int(url.replace('https://api.github.com/user/','').split('/')[0])
