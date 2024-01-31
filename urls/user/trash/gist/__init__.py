from django.urls import include, path

from views.user.trash import gist as views

urlpatterns = [
    path('', views.View.as_view()),
]
