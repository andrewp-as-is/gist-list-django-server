from django.urls import include, path

from views.user.gists import languages as views

urlpatterns = [
    path('', views.View.as_view()),
]
