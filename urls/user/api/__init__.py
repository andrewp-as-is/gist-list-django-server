from django.urls import include, path

from views.user import api as views

urlpatterns = [
    path('/id.txt', include('urls.user.api.id')),
    path('/clone.txt', include('urls.user.api.clone')),
    path('/description.txt', include('urls.user.api.description')),
    path('/download.txt', include('urls.user.api.download')),
    path('', views.ApiView.as_view()),
]
