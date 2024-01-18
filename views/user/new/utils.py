from django.db.models import F

from base.apps.github.models import User

def update_user_gists_count(user_id,is_public):
    kwargs = dict(public_gists_count=F('public_gists_count')+1)
    if not is_public:
        kwargs = dict(private_gists_count=F('private_gists_count')+1)
    User.objects.filter(id=user_id).update(**kwargs)
