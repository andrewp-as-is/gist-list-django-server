from django.urls import path

from views.user import following as views

urlpatterns = [
    path('', views.View.as_view()),
]
