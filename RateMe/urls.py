from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from main import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.start),
    # url(r'^RateMe/', include('RateMe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login', {'extra_context': {'next':'/'}}),
    url(r'^login_form/$', views.login),
    url(r'^logout/$', logout),
    url(r'^rate/$', views.rate),
    url(r'^(\w+)/$', views.profile),
)
