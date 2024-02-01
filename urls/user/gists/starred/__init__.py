from django.urls import include, path

from views.user.gists import starred as views

urlpatterns = [
    path('/tags', include('urls.user.gists.starred.tags')),
    path('', views.View.as_view()),
]
