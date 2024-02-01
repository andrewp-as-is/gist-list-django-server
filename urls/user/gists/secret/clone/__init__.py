from django.urls import include, path

from views.user.gists.secret import clone as views

urlpatterns = [
    path('', views.View.as_view()),
]
