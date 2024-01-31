from base.apps.github.models import GistFileContent, Trash
from django.views.generic.base import TemplateView
from ...mixins import UserMixin

class View(UserMixin,TemplateView):
    template_name = "user/trash/gist/gist.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gist_id = self.kwargs['gist_id']
        try:
            trash = Trash.objects.get(gist_id=gist_id,)
        except Trash.DoesNotExist:
            # todo: 404
            pass
        file_list = []
        file_content_list = list(GistFileContent.objects.filter(gist_id=gist_id))
        filename2backup = {fc.filename:True for fc in file_content_list}
        context_data = context.get('context_data',{})
        context_data['trash'] = trash
        print('trash.filename_list: %s' % trash.filename_list)
        for i,filename in enumerate(trash.filename_list,0):
            local_raw_url = "/%s/%s/raw/%s" % (self.github_user.login,gist_id,filename)
            language, size = None, None
            if trash.language_list and len(trash.language_list)>i:
                language = trash.language_list[i]
            if trash.file_size_list and i>=len(trash.file_size_list):
                size = gist.file_size_list[i]
            print('language: %s' % language)
            backup = filename2backup.get(filename,None)
            danger = False
            if size and size>1024*1024: # 1Mb
                danger = True
            file_list+=[dict(
                filename=filename,
                size=42,
                language=language,
                local_raw_url=local_raw_url,
                danger=danger
            )]
        context_data['file_list'] = file_list
        context['context_data'] = context_data
        return context
