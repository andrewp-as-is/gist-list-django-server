from django.urls import path

from views.user import clone as views

app_name = 'clone'

urlpatterns = [
    path('', views.View.as_view()),
]
