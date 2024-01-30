from django.urls import path

from views import robots_txt as views

urlpatterns = [
    path('', views.View.as_view()),
]
