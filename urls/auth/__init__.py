from django.urls import include, path

urlpatterns = [
    path('github/', include('urls.auth.github')),
]
