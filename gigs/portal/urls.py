from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView, TemplateView
from gigs.gig_registry.models import Gig
from django.contrib.auth.views import logout

urlpatterns = patterns(
    'gigs.portal.views',
    url(r'^$', TemplateView.as_view(template_name='portal/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='portal/about.html'), name='about'),
    url(r'^contact/$', TemplateView.as_view(template_name='portal/contact.html'), name='contact'),
    url(r'^index/$', ListView.as_view(queryset=Gig.objects.all().order_by('start'),template_name="portal/index.html"), name='index'),
    url(r'^gig/(?P<pk>\d+)/$', DetailView.as_view(model=Gig, template_name="portal/gig_detail.html")),
    url(r'^login/$', 'portal_login', name='login'), 
    url(r'^logout/$', logout, {'next_page':'/'}, name='logout'), 
)
