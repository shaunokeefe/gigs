from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView, TemplateView
from gigs.gig_registry.models import Gig

urlpatterns = patterns(
    'search.views.',
    url(r'^$', TemplateView.as_view(template_name='portal/home.html'), name='home'),
)
