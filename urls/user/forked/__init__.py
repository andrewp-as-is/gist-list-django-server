from django.urls import include, path

from views.user import forked as views

urlpatterns = [
    path('', views.ListView.as_view()),
]
