from django.urls import include, path

from views.user.gists import clone as views

urlpatterns = [
    path('', views.View.as_view()),
]
