from django.urls import include, path

from views.user.following import refresh as views

urlpatterns = [
    path('', views.View.as_view()),
]
