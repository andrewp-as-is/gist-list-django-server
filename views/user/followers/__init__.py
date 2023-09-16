from django.db.models import Q

from base.apps.github.models import User, Follower
from base.apps.github_matview.models import Follower

from views.base import ListView
from ..mixins import UserMixin

class ListView(UserMixin,ListView):
    context_object_name = "follower_list"
    template_name = "user/followers/follower_list.html"

    def get_queryset(self,**kwargs):
        qs = Follower.objects.filter(user_id=self.github_user.id)
        q = self.request.GET.get('q','').strip()
        if q:
            qs = qs.filter(
                Q(**{'login__icontains':q}) |
                Q(**{'name__icontains':q}) |
                Q(**{'company__icontains':q}) |
                Q(**{'location__icontains':q})
            )
        qs = qs.select_related('follower')
        return qs
        # return qs.order_by(Lower('login'))


