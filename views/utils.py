from base.apps.github_gist_matview.models import Gist as MatviewGist
from base.apps.github_gist_new_matview.models import Gist as NewMatviewGist

def get_gist_model(user_id):
    if not user_id:
        return MatviewGist
    if NewMatviewGist.objects.filter(owner_id=user_id).only('id').first():
        return NewMatviewGist
    return MatviewGist

def get_url(request,**kwargs):
    data = {k:v for k,v in request.GET.items()}
    data.update(kwargs)
    params = []
    for k in list(data.keys()):
        params.append('%s=%s' % (k,data[k]))
    return request.path+'?'+'&'.join(params)
