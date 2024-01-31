from django.urls import include, path

from views.user import trash as views

urlpatterns = [
    path('/<str:gist_id>', include('urls.user.trash.gist')),
    path('', views.View.as_view()),
]
