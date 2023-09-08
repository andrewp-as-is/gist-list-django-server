from django.urls import path

from views.token import delete as views

urlpatterns = [
    path('', views.View.as_view()),
]
