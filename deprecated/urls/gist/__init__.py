from django.urls import path

from views import gist as views

app_name = 'gist'

urlpatterns = [
    path('create', views.GistCreateView.as_view(),name='gist_create'),
    path('<str:pk>/delete', views.GistTrashView.as_view(),name='gist_delete'),
    path('<str:pk>/star', views.GistStarView.as_view(),name='gist_star'),
    path('<str:pk>/unstar', views.GistUnstarView.as_view(),name='gist_unstar'),
]
