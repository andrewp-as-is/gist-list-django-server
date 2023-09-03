from django.db.models import F, Q
from django.db.models.functions import Lower

from base.apps.github.models import User, Follower

from views.base import ListView
from views.user.mixins import UserMixin

class ListView(UserMixin,ListView):
    context_object_name = "user_list"
    template_name = "user/followers/user_list.html"
    paginate_by = 100

    def get_queryset(self,**kwargs):
        qs = User.objects.filter(
            id__in=Follower.objects.filter(user_id=self.github_user.id).values_list('follower_id',flat=True)
        )
        q = self.request.GET.get('q','').strip()
        if q:
            qs = qs.filter(
                Q(**{'login__icontains':q}) |
                Q(**{'name__icontains':q}) |
                Q(**{'company__icontains':q}) |
                Q(**{'location__icontains':q})
            )
        return qs.order_by(Lower('login'))


