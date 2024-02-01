from django.urls import include, path

from views.user.gists import public as views

urlpatterns = [
    path('/clone', include('urls.user.gists.public.clone')),
    path('/clone.sh', include('urls.user.gists.public.clone_sh')),
    path('', views.View.as_view()),
]
