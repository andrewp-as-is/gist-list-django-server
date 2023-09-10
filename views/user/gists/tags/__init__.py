from base.apps.tag.models import Tag

from views.base import TemplateView
from views.details import Details
from views.user.mixins import UserMixin
from views.user.gists.utils import get_queryset_base, get_tag_stat
from utils import get_gist_tag_model


def get_tag_list(total_count,stat):
    tag_id_list = list(stat.keys())
    id2count = {tag_id:count for tag_id,count in stat.items()}
    tag_list = list(Tag.objects.filter(id__in=tag_id_list))
    for tag in tag_list:
        tag.count = id2count.get(tag.id,0)
        tag.percent = round((tag.count/total_count)*100,1)
    return tag_list


class View(UserMixin,TemplateView):
    template_name = "user/gists/tags/tag_list.html"

    def get_gist_queryset(self):
        return get_queryset_base(self.request,self.github_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gist_queryset = self.get_gist_queryset()
        total_count = gist_queryset.count()
        gist_model = gist_queryset.model
        gist_tag_model = get_gist_tag_model(gist_model._meta.app_label)
        stat = get_tag_stat(gist_queryset,gist_tag_model)
        tag_list = get_tag_list(total_count,stat)
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
