from django.urls import path

from views.user import followers as views

urlpatterns = [
    path('', views.View.as_view()),
]
