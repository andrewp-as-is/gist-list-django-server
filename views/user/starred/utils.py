from base.apps.github_gist_star_matview.models import Gist as MatviewGist
from base.apps.github_gist_star_new_matview.models import Gist as NewMatviewGist

def get_gist_star_model(stargazer_id):
    if stargazer_id:
        if NewMatviewGist.objects.filter(stargazer_id=stargazer_id).only('id').first():
            return NewMatviewGist
    return MatviewGist
