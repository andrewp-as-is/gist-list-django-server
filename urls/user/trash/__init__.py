from django.urls import path

from views.user import trash as views

urlpatterns = [
    path('', views.View.as_view()),
]
