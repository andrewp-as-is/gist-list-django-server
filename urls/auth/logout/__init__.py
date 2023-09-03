from django.urls import include, path

from views.auth import logout as views

urlpatterns = [
    path('', views.View.as_view()),
]
