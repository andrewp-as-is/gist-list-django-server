from django.urls import path

from views import pricing as views


urlpatterns = [
    path('', views.View.as_view()),
]
