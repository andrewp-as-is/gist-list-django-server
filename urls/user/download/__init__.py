from django.urls import path

from views.user import download as views

urlpatterns = [
    path('', views.View.as_view()),
]
