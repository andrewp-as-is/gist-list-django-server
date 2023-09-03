from django.urls import path

from views import gist_id as views

app_name = 'id'

urlpatterns = [
    path('', views.View.as_view()),
]
