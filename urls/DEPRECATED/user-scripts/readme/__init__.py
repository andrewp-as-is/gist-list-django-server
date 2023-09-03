from django.urls import include, path

from views.user.scripts import readme as views

urlpatterns = [
    path('', views.ReadmeView.as_view()),
]
