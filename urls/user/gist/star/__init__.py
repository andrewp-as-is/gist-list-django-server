from django.urls import include, path

from views.user.gist import star as views

urlpatterns = [
    path('', views.View.as_view()),
]
