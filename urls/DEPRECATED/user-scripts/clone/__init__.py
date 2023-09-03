from django.urls import include, path

from views.user.scripts import clone as views

urlpatterns = [
    path('', views.CloneView.as_view()),
]
