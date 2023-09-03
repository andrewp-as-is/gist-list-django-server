from base.apps.github.models import Gist

def update_user_stars(user_id):
    count = GistStar.objects.filter(user_id=user_id).count()
    User.objects.filter(id=user_id).update(
        stars_count=count,
    )
