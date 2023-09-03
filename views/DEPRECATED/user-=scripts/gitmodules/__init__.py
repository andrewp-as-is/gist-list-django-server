from base.apps.github.models import Gist
from views.user.base import LinesView

class GitmodulesView(LinesView):

    def get_queryset(self):
        order_by = ['description','id'] if self.request.GET.get('name','')=='description' else ['id']
        return Gist.objects.filter(owner_id=self.github_user.id).order_by(*order_by)

    def iter_lines(self):
        get_method = self.request.GET.get('method','ssh') or 'ssh'
        get_path = self.request.GET.get('path','description')
        yield '# curl -s https://gists42.com/%s/scripts/gitmodules.sh | sh -v' % (self.login,)
        yield '# method: https, ssh'
        yield '# name: id, description'
        yield ''
        for gist in self.qs:
            path = '"%s"' % gist.description if gist.description and get_path=='description' else gist.id
            url = 'git@gist.github.com:%s.git' % gist.id
            yield 'git submodule -q add %s %s' % (url,path,)
