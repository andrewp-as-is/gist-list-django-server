from views.user.gists import View as _View
from ..mixins import UserMixin
from .utils import get_top_language_list, get_most_used_tag_list

class View(_View):
    paginate_by = 10
    template_name = "user/overview/overview.html"

    def get_details_view_menu_item_list(self):
        pass

    def get_popular_gist_list(self):
        qs = self.get_queryset_base().filter(stargazers_count__gt=0,public=True)
        return list(qs.order_by('-stargazers_count')[0:5])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = context.get('context_data',{})
        context_data['top_language_list'] = get_top_language_list(self.github_user_stat,self.secret)
        context_data['most_used_tag_list'] = get_most_used_tag_list(self.github_user_stat,self.secret)
        context_data['popular_gist_list'] = self.get_popular_gist_list()
        context['context_data'] = context_data
        return context
