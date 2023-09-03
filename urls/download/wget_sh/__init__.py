from django.urls import path

from views.download import wget_sh as views

app_name = 'wget_sh'

urlpatterns = [
    path('', views.View.as_view()),
]
