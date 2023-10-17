from django.urls import include, path

from views.user.gist import refresh as views

urlpatterns = [
    path('', views.View.as_view()),
]
