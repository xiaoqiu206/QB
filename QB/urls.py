from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'QB.views.home', name='home'),
    # url(r'^QB/', include('QB.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'recharge.views.index'),
    url(r'^login/', 'recharge.views.login'),
    url(r'^list', 'recharge.views.rechargeList'),
    url(r'^handle_order', 'recharge.views.handle_order')
)
