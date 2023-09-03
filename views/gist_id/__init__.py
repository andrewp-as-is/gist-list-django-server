from django.http import HttpResponse

from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from base.apps.github.models import User
from views.utils import get_gist_model

class View(TemplateView):
    template_name = 'gist-id/gist_id.html'

    def dispatch(self, request, *args, **kwargs):
        self.login = self.request.GET.get('login','')
        if self.request.user.is_authenticated and not self.login:
            return redirect('/gist-id?login=%s' % request.user.login)
        self.github_user = None
        if self.login:
            try:
                self.github_user = User.objects.get(login=self.login)
            except User.DoesNotExist:
                pass
        return super().dispatch(request, *args, **kwargs)

    def get_model(self):
        if self.github_user:
            return get_gist_model(user_id=self.github_user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['github_user'] = self.github_user
        if self.github_user:
            model = self.get_model()
            context['unknown_version_gist_list'] = list(model.objects.filter(
                owner_id=self.github_user.id,
                version__isnull=True
            ).order_by('id'))
        return context
