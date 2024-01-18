from views.user.gists import View as ListView

class View(ListView):
    paginate_by = 100000
