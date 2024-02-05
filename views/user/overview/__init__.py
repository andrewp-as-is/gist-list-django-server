from views.user.gists import View as _View
from ..mixins import UserMixin

SORT_ITEM_LIST = [
    # {'key':'stars','text':'Stars'},
    # {'key':'forks','text':'Forks'},
    {'value':'-created','description':'Recently created'},
    {'value':'-updated','description':'Recently updated'},
    {'value':'-stargazers','description':'Most stars'},
    #{'value':'-forks','description':'Most forks'},
   # {'value':'-comments','description':'Most comments'},
    #{'value':'created','description':'Least recently created'},
    #{'value':'updated','description':'Least recently updated'},
    {'value':'filename','description':'Filename'},
    {'value':'description','description':'Description'},
    #{'value':'id','description':'ID'},
]


class View(_View):
    paginate_by = 10
    template_name = "user/overview/overview.html"

    def get_details_sort_menu_item_list(self):
        return self.get_details_menu_item_list('sort',SORT_ITEM_LIST)

    def get_details_view_menu_item_list(self):
        pass

    def get_popular_gist_list(self):
        qs = self.get_queryset_base().filter(stargazers_count__gt=0,public=True)
        return list(qs.order_by('-stargazers_count')[0:5])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = context.get('context_data',{})
        context_data['popular_gist_list'] = self.get_popular_gist_list()
        details = context_data.get('details',{})
       # details['language'] = None
        #details['tag'] = None
        context_data['details'] = details
        context['context_data'] = context_data
        return context
