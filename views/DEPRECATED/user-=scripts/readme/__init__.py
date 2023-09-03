from base.apps.github.models import Gist
from views.user.base import LinesView

def get_url(gist):
    return 'https://gist.github.com/%s' % gist.id

def get_id(gist):
    return '[%s](%s)' % (gist.id,get_url(gist),)

def get_description(gist):
    url = get_url(gist)
    description = gist.description if gist.description else ''
    return '[%s](%s)' % (description,url,)

def get_files(gist,):
    url = get_url(gist)
    files = gist.filename if len(gist.get_files())==1 else gist.filename+', ...'
    return '[%s](%s)' % (files,url,)


class ReadmeView(LinesView):

    def get_queryset(self):
        order_by = ['description','id'] if self.request.GET.get('sort','')=='description' else ['id']
        return Gist.objects.filter(owner_id=self.github_user.id).order_by(*order_by)

    def iter_lines(self):
        colnames = (self.request.GET.get('columns','') or 'id,description,files').split(',')
        if not colnames:
            return
        if len(colnames)==1:
            colnames.append('-')
        yield '|'.join(colnames)
        yield '|'.join(list('-'*len(colnames)))
        for gist in self.qs:
            url = 'https://gist.github.com/%s/%s' % (self.login,gist.id,)
            cols = []
            for colname in colnames:
                if colname == '-':
                    cols.append('-')
                if colname == 'id':
                    cols.append(get_id(gist))
                if colname == 'description':
                    cols.append(get_description(gist))
                if colname == 'files':
                    cols.append(get_files(gist))
            yield '|'.join(cols)
