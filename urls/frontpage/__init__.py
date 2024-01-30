from django.urls import path

from views import frontpage as views

urlpatterns = [
    path('', views.View.as_view()),
]
