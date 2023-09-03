from django.urls import include, path

from views.user import refresh_status as views

urlpatterns = [
    path('', views.View.as_view()),
]
