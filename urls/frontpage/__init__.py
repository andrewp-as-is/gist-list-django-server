from django.urls import path

from views import frontpage as views

app_name = 'frontpage'

urlpatterns = [
    path('', views.View.as_view()),
]
