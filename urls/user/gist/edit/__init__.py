from django.urls import include, path

from views.user.gist import edit as views

urlpatterns = [
    path('', views.View.as_view()),
]
