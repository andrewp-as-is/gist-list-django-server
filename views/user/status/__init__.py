from django.views.generic.base import TemplateView

# from base.apps.github.models import UserInternalJobDetect, UserRequestJobDetect
from views.user.mixins import UserMixin

class View(UserMixin, TemplateView):
    template_name = 'user/status/status.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.github_user:
            user_id = self.github_user.id
            raise ValueError('UserInternalJobDetect -> todo')
            # context['request_job'] = UserRequestJobDetect.objects.filter(user_id=user_id).count()>0
            # context['internal_job'] = UserInternalJobDetect.objects.filter(user_id=user_id).count()>0
        return context
