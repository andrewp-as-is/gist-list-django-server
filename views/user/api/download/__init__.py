from views.user.base import LinesView


class DownloadView(LinesView):

    def iter_lines(self):
        for gist in self.qs:
            if gist.version:
                url = 'https://gist.github.com/%s/%s/archive/%s.zip' % (self.login,gist.id,gist.version,)
                yield url
