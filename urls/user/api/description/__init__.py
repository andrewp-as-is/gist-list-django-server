from django.urls import include, path

from views.user.api import description as views

urlpatterns = [
    path('', views.DescriptionView.as_view()),
]
