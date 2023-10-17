from django.urls import include, path

from views.user import secret as views

urlpatterns = [
    path('', views.View.as_view()),
]
