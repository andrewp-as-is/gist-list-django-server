from django.urls import include, path

from views.user.gists.public import clone_sh as views

urlpatterns = [
    path('', views.View.as_view()),
]
