from django.urls import path

from views import gist_id_txt as views

app_name = 'id_txt'

urlpatterns = [
    path('', views.View.as_view()),
]
