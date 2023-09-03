from views.base import TemplateView

class ErrorView(TemplateView):
    template_name = 'auth/error.html'
