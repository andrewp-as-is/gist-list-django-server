from django.urls import include, path

from views import token as views

app_name = 'token'

urlpatterns = [
    path('/delete', include('urls.token.delete')),
    path('', views.View.as_view()),
]
