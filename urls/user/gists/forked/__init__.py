from django.urls import include, path

from views.user.gists import forked as views

urlpatterns = [
    path('', views.View.as_view()),
]
