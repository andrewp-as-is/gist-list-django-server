from django.urls import include, path

from views.user.gist import delete as views

urlpatterns = [
    path('', views.DeleteView.as_view()),
]
