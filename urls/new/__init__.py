from django.urls import path

from views import new as views

app_name = 'home'

urlpatterns = [
    path('', views.View.as_view(),name='new'),
]
