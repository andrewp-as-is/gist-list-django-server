from django.urls import include, path

from views.user import followers as views

urlpatterns = [
    path('/refresh', include('urls.user.followers.refresh')),
    path('', views.View.as_view()),
]
