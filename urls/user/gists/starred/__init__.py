from django.urls import include, path

from views.user.gists import starred as views

urlpatterns = [
    path('/refresh', include('urls.user.gists.starred.refresh')),
    path('/tags', include('urls.user.gists.starred.tags')),
    path('', views.View.as_view()),
]
