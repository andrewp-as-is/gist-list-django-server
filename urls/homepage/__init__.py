from django.urls import path

from views import homepage as views

urlpatterns = [
    path('', views.View.as_view()),
]
