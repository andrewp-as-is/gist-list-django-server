from django.urls import include, path

from views.user import gists as views

urlpatterns = [
    path('/clone', include('urls.user.gists.clone')),
    path('/clone.sh', include('urls.user.gists.clone_sh')),
    path('/download', include('urls.user.gists.download')),
    path('/forked', include('urls.user.gists.forked')),
    path('/public', include('urls.user.gists.public')),
    path('/secret', include('urls.user.gists.secret')),
    path('/starred', include('urls.user.gists.starred')),
    path('/languages', include('urls.user.gists.languages')),
    path('/tags', include('urls.user.gists.tags')),
    path('', views.View.as_view()),
]
