from django.urls import path

from views import healthcheck as views


urlpatterns = [
    path('', views.View.as_view()),
]
