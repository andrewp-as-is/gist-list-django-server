from django.urls import path

from views import download as views

urlpatterns = [
    path('', views.View.as_view()),
]
