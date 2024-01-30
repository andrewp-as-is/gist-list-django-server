from django.urls import include, path

urlpatterns = [
    path('callback', include('urls.auth.github.callback')),
    path('redirect', include('urls.auth.github.redirect')),
]
