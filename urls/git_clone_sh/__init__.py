from django.urls import path

from views import git_clone_sh as views

app_name = 'git_clone_sh'

urlpatterns = [
    path('', views.View.as_view()),
]
