from django.contrib.auth.mixins import LoginRequiredMixin

from base.apps.github.models import Gist,GistFileContent
from views.base import TemplateView
from ..mixins import GistMixin

"""
/USER/GIST/delete
/USER/GIST/delete/confirm
"""

class View(LoginRequiredMixin,GistMixin,TemplateView):
    template_name = 'user/gist/delete/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gist = self.gist
        file_list = []
        file_content_list = list(GistFileContent.objects.filter(gist_id=gist.id))
        filename2backup = {fc.filename:True for fc in file_content_list}
        context_data = context.get('context_data',{})
        for i,filename in enumerate(gist.filename_list,0):
            raw_url = "https://gist.githubusercontent.com/%s/%s/raw/%s" % (self.github_user.login,gist.id,filename)
            local_raw_url = "/%s/%s/raw/%s" % (self.github_user.login,gist.id,filename)
            language, size = None, None
            if gist.language_list and i>=len(gist.language_list):
                language = gist.language_list[i]
            if gist.file_size_list and i>=len(gist.file_size_list):
                size = gist.file_size_list[i]
            backup = filename2backup.get(filename,None)
            danger = False
            if size and size>1024*1024: # 1Mb
                danger = True
            file_list+=[dict(
                filename=filename,
                size=42,
                language=language,
                raw_url=raw_url,
                local_raw_url=local_raw_url,
                danger=danger
            )]
        context_data['file_list'] = file_list
        context['context_data'] = context_data
        return context

