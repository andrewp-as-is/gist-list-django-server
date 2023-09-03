from django.urls import include, path
from views import status as views

app_name = 'status'

urlpatterns = [
    path('/history', include('urls.status.history')),
    path('', views.View.as_view()),
]
