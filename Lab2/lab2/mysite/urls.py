from django.conf.urls import patterns, include, url
#from django.conf.urls.defaults import *  (this is not supported in django1.6)
from addr_book.views import *
from django.contrib.auth.views import login, logout
from mysite import settings
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    (r'^add/$', addrecord),
    (r'^$', showrecord),
    (r'^delete/$', deleterecord),
    (r'^update/$', updaterecord),
    (r'^search/$', search),
    (r'^showmap/$', showmap),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/changepassword/$', chpwd),
    (r'^accounts/register/$', reg),
    #(r'^medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
