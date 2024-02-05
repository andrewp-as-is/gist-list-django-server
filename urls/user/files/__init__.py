from django.urls import path

from views.user import files as views

urlpatterns = [
    path('', views.View.as_view()),
]
