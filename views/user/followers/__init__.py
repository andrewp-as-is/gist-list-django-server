from views.base import ListView
from utils import get_follower_model
from ..mixins import UserMixin

class ListView(UserMixin,ListView):
    context_object_name = "follower_list"
    template_name = "user/followers/follower_list.html"

    def get_model(self):
        return get_follower_model(self.modification_matview_time)

    def get_queryset(self,**kwargs):
        model = self.get_model()
        print('model: %s' % model)
        qs = model.objects.filter(user_id=self.github_user.id)
        q = self.request.GET.get('q','').strip()
        if q:
            qs = qs.filter(
                Q(**{'follower__login__icontains':q}) |
                Q(**{'follower__name__icontains':q}) |
                Q(**{'follower__company__icontains':q}) |
                Q(**{'follower__location__icontains':q})
            )
        return qs.select_related('follower')
        # return qs.order_by(Lower('login'))


