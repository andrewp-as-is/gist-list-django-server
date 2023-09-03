from django.urls import path

from views import scripts as views

app_name = 'scripts'

urlpatterns = [
    path('', views.View.as_view()),
]
