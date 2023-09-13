from django.urls import path

from views import incident as views


urlpatterns = [
    path('', views.View.as_view()),
]
