from django.urls import include, path

from views.user import gist as views

urlpatterns = [
    path('/clone', include('urls.user.gist.clone')),
    path('/delete', include('urls.user.gist.delete')),
    path('/description', include('urls.user.gist.description')),
    path('/edit', include('urls.user.gist.edit')),
    path('/refresh', include('urls.user.gist.refresh')),
    path('/star', include('urls.user.gist.star')),
    path('/unstar', include('urls.user.gist.unstar')),
    path('', views.DetailView.as_view()),
]
