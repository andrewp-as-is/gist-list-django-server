from django.urls import include, path

from views.user.gist import unstar as views

urlpatterns = [
    path('', views.View.as_view()),
]
