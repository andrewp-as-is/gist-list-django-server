from django.urls import path

from views.download import curl_sh as views

app_name = 'curl_sh'

urlpatterns = [
    path('', views.View.as_view()),
]
