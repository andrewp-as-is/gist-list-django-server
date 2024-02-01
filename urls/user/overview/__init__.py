from django.urls import path

from views.user import overview as views

urlpatterns = [
    path('', views.View.as_view()),
]
