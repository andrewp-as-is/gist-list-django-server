from base.apps.github_matview.models import StarredGist
from base.apps.github_matview_new.models import StarredGist as NewStarredGist

def get_starred_gist_model(stargazer_id):
    if stargazer_id:
        if NewStarredGist.objects.filter(stargazer_id=stargazer_id).only('id').first():
            return NewStarredGist
    return StarredGist
