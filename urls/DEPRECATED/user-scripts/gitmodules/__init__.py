from django.urls import include, path

from views.user.scripts import gitmodules as views

urlpatterns = [
    path('', views.GitmodulesView.as_view()),
]
