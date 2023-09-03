from base.apps.github.models import Gist
from views.user.base import LinesView

class CloneView(LinesView):

    def get_queryset(self):
        order_by = ['description','id'] if self.request.GET.get('name','')=='description' else ['id']
        return Gist.objects.filter(owner_id=self.github_user.id).order_by(*order_by)

    def iter_lines(self):
        get_method = self.request.GET.get('method','ssh') or 'ssh'
        get_name = self.request.GET.get('name','description')
        yield '# curl -s "https://gists42.com/%s/clone.sh?method=%s&name=%s" | sh -v' % (self.login,get_method,get_name)
        yield '# method: https, ssh'
        yield '# name: id, description'
        yield ''
        for gist in self.qs:
            url = 'git@gist.github.com:%s.git' % gist.id
            name = '"%s"' % gist.description if gist.description and get_name=='description' else gist.id
            yield 'git clone -q %s %s' % (url,name,)
