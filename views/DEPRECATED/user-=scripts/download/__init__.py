from views.user.base import LinesView

class DownloadView(LinesView):

    def iter_lines(self):
        yield '# curl -s https://gists42.com/%s/scripts/download.sh | sh -v' % (self.login,)
        yield '# method: https, ssh'
        yield '# name: id, description'
        yield ''
        for gist in self.qs:
            if gist.version:
                url = 'https://gist.github.com/%s/%s/archive/%s.zip' % (self.login,gist.id,gist.version,)
                yield 'curl -L -s %s -o %s.zip' % (url,gist.id,)
