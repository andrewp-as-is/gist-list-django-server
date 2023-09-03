from django.urls import include, path

from views.auth.github import callback as views

urlpatterns = [
    path('', views.View.as_view()),
]
