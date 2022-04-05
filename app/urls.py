from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from garpix_page.views.page import PageView
from config.views import robots_txt, sitemap_view
from django.contrib.sitemaps.views import sitemap
from django.http import Http404
from multiurl import ContinueResolving, multiurl
from django.http import HttpResponse


urlpatterns = [
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    path('admin/backups/', include('dbbackup_ui.urls')),
    path('admin/', admin.site.urls),
    path('admin/auth/', include('django.contrib.auth.urls')),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, sitemap_view(), name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^_nested_admin/', include('nested_admin.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^cmsmagazine8dbc8898b2f57ed5aa99f9b830172491\.txt', lambda x: HttpResponse("8dbc8898b2f57ed5aa99f9b830172491", content_type="text/plain; charset=utf8")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += i18n_patterns(
    multiurl(
        path('', PageView.as_view()),
        re_path(r'^(?P<url>.*?)$', PageView.as_view(), name='page'),
        re_path(r'^(?P<url>.*?)/$', PageView.as_view(), name='page'),
        catch=(Http404, ContinueResolving),
    ),
    prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX,
)
