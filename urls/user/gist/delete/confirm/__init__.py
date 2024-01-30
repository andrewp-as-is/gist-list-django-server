from django.urls import include, path

from views.user.gist.delete import confirm as views

urlpatterns = [
    path('', views.View.as_view()),
]
