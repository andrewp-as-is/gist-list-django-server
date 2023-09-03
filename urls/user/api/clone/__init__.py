from django.urls import include, path

from views.user.api import clone as views

urlpatterns = [
    path('', views.CloneView.as_view()),
]
