from django.urls import include, path

from views.user.api import id as views

urlpatterns = [
    path('', views.IdView.as_view()),
]
