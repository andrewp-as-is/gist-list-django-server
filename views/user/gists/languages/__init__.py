from base.apps.github.models import Language

from django_postgres_database_size.models import DatabaseSize
from views.details import Details
from views.user.gists import View as ListView
from views.user.gists.utils import get_language_stat


LANGUAGE_ID2LANGUAGE = {l.id:l for l in Language.objects.all()}


def get_language_list(total_count,stat):
    language_list = []
    for language_id,count in stat.items():
        language = LANGUAGE_ID2LANGUAGE.get(language_id,None)
        if language:
            language.count = count
            language.percent = round((count/total_count)*100,1)
            language_list+=[language]
    return language_list

class View(ListView):
    template_name = "user/gists/languages/language_list.html"

    def get_gist_queryset(self):
        return get_queryset_base(self.request,self.github_user)

    def get_context_data(self, **kwargs):
        print(list(DatabaseSize.objects.all()))
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset_base()
        total_count = qs.count()
        stat = get_language_stat(qs,self.gist_language_model)
        language_list = get_language_list(total_count,stat)
        menu_item_list = [
            {'value':'count','text':'Most gists'},
            {'value':'name','text':'Name'},
        ]
        context['sort_details'] = Details(self.request,
            name='Sort',
            summary_css_class="btn-link color-fg-muted",
            menu_title = 'Select order',
            menu_item_list=menu_item_list
        )
        context['languages_count'] = len(stat)-1
        unknown_count = total_count-len(stat)+1
        language_list = list(sorted(
            language_list,
            key=lambda l:-l.count if self.request.GET.get('sort','count')=='count' else l.slug
        ))
        if unknown_count:
            language_list = [{
                'slug':None,
                'count':unknown_count,
                'percent':round((unknown_count/total_count)*100,1)
            }]+language_list
        context['language_list'] = language_list
        return context
