
from views.user.gists import View as ListView
# from views.user.gists.utils import get_tag_stat


class View(ListView):
    template_name = "user/gists/tags/tag_list.html"

    def get_gist_queryset(self):
        return get_queryset_base(self.request,self.github_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset_base()
        total_count = qs.count()
        stat = get_tag_stat(qs,self.gist_tag_model)
        tag_list = get_tag_list(total_count,stat)
        menu_item_list = [
            {'value':'count','text':'Most gists'},
            {'value':'name','text':'Name'},
        ]
       # context['sort_details'] = Details(self.request,
       #     name='Sort',
       #     menu_item_list=menu_item_list
       # )
        context['tags_count'] = len(stat)-1
        unknown_count = total_count-len(stat)+1
        tag_list = list(sorted(
            tag_list,
            key=lambda t:-t.count if self.request.GET.get('sort','count')=='count' else t.slug
        ))
        if unknown_count:
            tag_list = [{
                'slug':None,
                'count':unknown_count,
                'percent':round((unknown_count/total_count)*100,1)
            }]+tag_list
        context['tag_list'] = tag_list
        return context
