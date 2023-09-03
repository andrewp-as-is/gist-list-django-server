from django.urls import path

from views.user import following as views

app_name = 'following'

urlpatterns = [
    path('', views.ListView.as_view(),name='user_list'),
]
