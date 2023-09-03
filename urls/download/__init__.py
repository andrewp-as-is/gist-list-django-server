from django.urls import include, path

from views import download as views

app_name = 'download'

urlpatterns = [
    path('/curl.sh', include('urls.download.curl_sh')),
    path('/wget.sh', include('urls.download.wget_sh')),
    path('', views.View.as_view()),
]
