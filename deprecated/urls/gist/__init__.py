from django.urls import path

from views import gist as views

urlpatterns = [
    path('create', views.View.as_view()),
    path('<str:pk>/delete', views.View.as_view()),
    path('<str:pk>/star', views.View.as_view()),
    path('<str:pk>/unstar', views.View.as_view()),
]
