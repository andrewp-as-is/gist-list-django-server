from django.urls import include, path

from views.user import gists as views

urlpatterns = [
    path('/languages', include('urls.user.gists.languages')),
    path('/tags', include('urls.user.gists.tags')),
    path('', views.View.as_view()),
]
