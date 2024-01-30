from django.urls import path
from views.status import history as views

urlpatterns = [
    path('', views.View.as_view()),
]
