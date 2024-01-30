from django.urls import path

from views.user import followers as views

urlpatterns = [
    path('', views.ListView.as_view(),name='user_list'),
]
