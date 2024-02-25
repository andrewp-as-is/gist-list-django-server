from django.urls import include, path

from views.user import following as views

urlpatterns = [
    path('/refresh', include('urls.user.following.refresh')),
    path('', views.View.as_view()),
]
