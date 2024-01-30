from django.urls import path

from views import users as views

urlpatterns = [
    path('', views.View.as_view()),
]
