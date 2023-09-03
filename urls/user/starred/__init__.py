from django.urls import include, path

from views.user import starred as views

urlpatterns = [
    path('', views.ListView.as_view()),
]
