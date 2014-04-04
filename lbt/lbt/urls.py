from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lbt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^get_haproxy_config$', "at.views.get_haproxy_config"),
    url(r'^report_lbresult$', "at.views.report_lbresult"),
    url(r'^lb_report$', "at.views.lb_report"),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    )

urlpatterns += patterns('',
    url(r'^', "echo.views.echo"),
)
