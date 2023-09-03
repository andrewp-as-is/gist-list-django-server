from views.user.base import LinesView

class IdView(LinesView):

    def iter_lines(self):
        for gist in self.qs:
            if gist.version:
                yield gist.id
