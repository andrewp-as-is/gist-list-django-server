from django.urls import include, path

from views.user.gist import delete as views

urlpatterns = [
    path('/confirm', include('urls.user.gist.delete.confirm')),
    path('', views.View.as_view()),
]
