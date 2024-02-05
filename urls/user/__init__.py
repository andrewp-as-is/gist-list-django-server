from django.urls import include, path

from views import user as views

urlpatterns = [
    path('/api', include('urls.user.api')),
    path('/files', include('urls.user.files')),
    path('/gists', include('urls.user.gists')),
    path('/gists.json', include('urls.user.gists_json')),
    path('new', include('urls.user.new')),
    path('/refresh', include('urls.user.refresh')),
    path('/status', include('urls.user.status')),
    path('/followers',      include('urls.user.followers')),
    path('/following',      include('urls.user.following')),
    path('/languages',   include('urls.user.gists.languages')),
    path('/tags',   include('urls.user.gists.tags')),
    path('/trash', include('urls.user.trash')),
    path('/<str:pk>', include('urls.user.gist')),
    path('',   include('urls.user.overview')),
]
