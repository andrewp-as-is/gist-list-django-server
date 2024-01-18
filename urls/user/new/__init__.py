from django.urls import path

from views.user import new as views

urlpatterns = [
    path('', views.View.as_view()),
]
