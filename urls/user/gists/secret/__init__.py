from django.urls import include, path

from views.user.gists import secret as views

urlpatterns = [
    path('/clone', include('urls.user.gists.secret.clone')),
    path('/clone.sh', include('urls.user.gists.secret.clone_sh')),
    path('', views.View.as_view()),
]
