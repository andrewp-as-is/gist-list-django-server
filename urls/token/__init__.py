from django.urls import path

from views import token as views

app_name = 'token'

urlpatterns = [
    path('', views.View.as_view()),
]
