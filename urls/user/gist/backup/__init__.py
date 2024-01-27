from django.urls import include, path

from views.user.gist import backup as views

urlpatterns = [
    path('', views.View.as_view()),
]
