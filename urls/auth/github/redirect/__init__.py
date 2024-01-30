from django.urls import include, path

from views.auth.github import redirect as views

urlpatterns = [
    path('', views.View.as_view()),
]
