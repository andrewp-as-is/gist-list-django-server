from django.urls import include, path

from views import user as views

app_name = 'user'

urlpatterns = [
    path('/api', include('urls.user.api')),
    path('/clone', include('urls.user.clone')),
    path('/download', include('urls.user.download')),
    path('/forked', include('urls.user.forked')),
    path('/gists.json', include('urls.user.gists_json')),
    path('new', include('urls.user.new')),
    path('/public', include('urls.user.public')),
    path('/secret', include('urls.user.secret')),
    path('/starred', include('urls.user.starred')),
    path('/refresh', include('urls.user.refresh')),
    path('/status', include('urls.user.status')),
    path('/followers',      include('urls.user.followers')),
    path('/following',      include('urls.user.following')),
    path('/languages',   include('urls.user.gists.languages')),
    path('/tags',   include('urls.user.gists.tags')),
    path('/trash', include('urls.user.trash')),
    path('/<str:pk>', include('urls.user.gist')),
    path('',   include('urls.user.gists')),
]
