from django.urls import include, path

from views.user.gists import download as views

urlpatterns = [
    path('', views.View.as_view()),
]
