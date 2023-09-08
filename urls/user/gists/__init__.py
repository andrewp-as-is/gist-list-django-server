from django.urls import include, path

from views.user import gists as views

urlpatterns = [
    path('/tags', include('urls.user.gists.tags')),
    path('', views.View.as_view()),
]
