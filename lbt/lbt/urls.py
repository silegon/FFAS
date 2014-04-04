from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lbt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^get_haproxy_config$', "at.views.get_haproxy_config"),
    url(r'^report_lbresult$', "at.views.report_lbresult"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', "echo.views.echo"),
)
