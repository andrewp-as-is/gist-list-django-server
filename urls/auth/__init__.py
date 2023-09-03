from django.urls import include, path

app_name = __name__.split('.')[-1]

urlpatterns = [
    path('github/', include('urls.auth.github')),
    path('logout', include('urls.auth.logout')),
]
