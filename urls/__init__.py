from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from django.urls import include, path, register_converter



urlpatterns = [
    path("admin/", admin.site.urls),

    path('status', include('urls.status')),
    path('robots.txt', include('urls.robots_txt')),

    path('auth/', include('urls.auth')),
    path('login', RedirectView.as_view(url='auth/github/redirect', permanent=False)),
    path('logout', LogoutView.as_view(
        next_page=(getattr(settings,'LOGOUT_REDIRECT_URL','/') or '/')
    )),

    # path('clone', include('urls.clone')),

    path('download', include('urls.download')),
    path('download.txt', include('urls.download_txt')),

    path('git-clone.sh', include('urls.git_clone_sh')),
    path('git-clone', include('urls.git_clone')),

    path('gist-id', include('urls.gist_id')),
    path('gist-id.txt', include('urls.gist_id_txt')),

    path('new', include('urls.new')),
    path('incident', include('urls.incident')),
    path('pricing', include('urls.pricing')),
    path('scripts', include('urls.scripts')),
    path('search', include('urls.search')),
    path('healthcheck', include('urls.healthcheck')),
    path('status', include('urls.status')),
    path('token', include('urls.token')),
    path('users', include('urls.users')),

    path('<slug:login>/', include('urls.user')),
    path('<slug:login>', include('urls.user')),

    path('', include('urls.frontpage')),
]

if settings.DEBUG:
    if settings.STATIC_URL and settings.STATIC_ROOT:
        urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if settings.MEDIA_URL and settings.MEDIA_ROOT:
        urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
