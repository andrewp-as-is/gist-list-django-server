from django.urls import include, path

from views.user.gists.starred import refresh as views

urlpatterns = [
    path('', views.View.as_view()),
]
