from django.urls import path

from views.user import followers as views

app_name = 'followers'

urlpatterns = [
    path('', views.ListView.as_view(),name='user_list'),
]
