from django.urls import path

from views.user import gists_json as views

urlpatterns = [
    path('', views.View.as_view()),
]
