from django.urls import include, path

from views.user import starred as views

urlpatterns = [
    path('/tags', include('urls.user.starred.tags')),
    path('', views.View.as_view()),
]
