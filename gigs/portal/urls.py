from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView, TemplateView
from gigs.gig_registry.models import Gig, Band, Venue, Location
from django.contrib.auth.views import logout

urlpatterns = patterns(
    'gigs.portal.views',
    url(r'^$', TemplateView.as_view(template_name='portal/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='portal/about.html'), name='about'),
    url(r'^contact/$', TemplateView.as_view(template_name='portal/contact.html'), name='contact'),
    url(r'^index/$', ListView.as_view(queryset=Gig.objects.all().order_by('start'),template_name="portal/index.html"), name='index'),
    url(r'^gig/(?P<pk>\d+)/$', DetailView.as_view(model=Gig, template_name="portal/gig_detail.html"), name='portal_gig_detail'),
    url(r'^band/(?P<pk>\d+)/$', DetailView.as_view(model=Band, template_name="portal/band_detail.html"), name='portal_band_detail'),
    url(r'^venue/(?P<pk>\d+)/$', DetailView.as_view(model=Venue, template_name="portal/venue_detail.html"), name='portal_venue_detail'),
    url(r'^location/(?P<pk>\d+)/$', DetailView.as_view(model=Location, template_name="portal/location_detail.html"), name='portal_location_detail'),
    url(r'^login/$', 'portal_login', name='login'), 
    url(r'^logout/$', logout, {'next_page':'/'}, name='logout'), 
)
