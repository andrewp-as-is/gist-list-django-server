from django.urls import include, path

from views.user import refresh_stat as views

urlpatterns = [
    path('', views.View.as_view()),
]
