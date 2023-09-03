from django.urls import path

from views import search as views

urlpatterns = [
    path('', views.View.as_view()),
]
