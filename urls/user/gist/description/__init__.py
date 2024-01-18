from django.urls import include, path

from views.user.gist import description as views

urlpatterns = [
    path('', views.View.as_view()),
]
