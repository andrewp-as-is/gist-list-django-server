from django.urls import path

from views.gist import GistCreateView

urlpatterns = [
    path('', GistCreateView.as_view()),
]
