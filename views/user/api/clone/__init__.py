from views.user.base import LinesView

class CloneView(LinesView):

    def iter_lines(self):
        method = self.request.GET.get('method','ssh') or 'ssh'
        for gist in self.qs:
            url = 'git@gist.github.com:%s.git' % gist.id
            yield url
