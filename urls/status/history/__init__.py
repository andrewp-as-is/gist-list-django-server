from django.urls import path
from views.status import history as views

app_name = 'history'

urlpatterns = [
    path('', views.View.as_view()),
]
