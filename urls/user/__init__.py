from django.urls import include, path

from views import user as views

app_name = 'user'

urlpatterns = [
    path('/clone', include('urls.user.clone')),
    path('/forked', include('urls.user.forked')),
    path('/public', include('urls.user.public')),
    path('/secret', include('urls.user.secret')),
    path('/starred', include('urls.user.starred')),
    path('/refresh', include('urls.user.refresh')),
    path('/status', include('urls.user.status')),
    path('/followers',      include('urls.user.followers')),
    path('/following',      include('urls.user.following')),
    path('/languages',   include('urls.user.gists.languages')),
    path('/tags',   include('urls.user.gists.tags')),
    path('/<str:pk>', include('urls.user.gist')),
    path('',   include('urls.user.gists')),
]
