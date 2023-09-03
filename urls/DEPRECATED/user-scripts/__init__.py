from django.urls import include, path

from views.user import scripts as views

urlpatterns = [
    path('/clone.sh', include('urls.user.scripts.clone')),
    path('/download.sh', include('urls.user.scripts.download')),
    path('/gitmodules.sh', include('urls.user.scripts.gitmodules')),
    path('/readme.md', include('urls.user.scripts.readme')),
    path('', views.ScriptsView.as_view()),
]
