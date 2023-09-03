from django.urls import include, path

app_name = __name__.split('.')[-1]

urlpatterns = [
    path('callback', include('urls.auth.github.callback')),
    path('redirect', include('urls.auth.github.redirect')),
]
