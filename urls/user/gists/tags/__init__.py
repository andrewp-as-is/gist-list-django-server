from django.urls import include, path

from views.user.gists import tags as views

urlpatterns = [
    path('', views.View.as_view()),
]
