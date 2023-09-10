from django.urls import path

from views import users as views

app_name = 'users'

urlpatterns = [
    path('', views.View.as_view()),
]
