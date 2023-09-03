from views.user.base import LinesView


class DescriptionView(LinesView):

    def iter_lines(self):
        for gist in self.qs:
            yield '%s,%s' % (gist.id,gist.description)
