from django.urls import include, path

from views.auth.github import redirect as views

app_name = __name__.split('.')[-1]

urlpatterns = [
    path('', views.View.as_view()),
]
