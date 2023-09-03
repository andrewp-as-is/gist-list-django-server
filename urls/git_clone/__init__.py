from django.urls import path

from views import git_clone as views

app_name = 'git_clone'

urlpatterns = [
    path('', views.View.as_view()),
]
