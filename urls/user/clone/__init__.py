from django.urls import path

from views.user import clone as views

urlpatterns = [
    path('', views.View.as_view()),
]
