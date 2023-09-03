from django.urls import path

from views import download_txt as views

app_name = 'download_txt'

urlpatterns = [
    path('', views.View.as_view()),
]
