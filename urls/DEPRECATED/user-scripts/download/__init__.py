from django.urls import include, path

from views.user.scripts import download as views

urlpatterns = [
    path('', views.DownloadView.as_view()),
]
