from django.urls import path

from views import robots_txt as views

app_name = 'robots'

urlpatterns = [
    path('', views.View.as_view()),
]
