
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from gigs.portal import urls as portal_urls
from gigs.search import urls as search_urls
from gigs.gig_registry.models import Gig, Venue, Location

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'', include(portal_urls)),
    (r'^admin/', include(admin.site.urls)),
    (r'^search/', include(search_urls)),
    (r'^export_gigs/$', 'django_tablib.views.export', {
            'model': Gig,
            }),
    (r'^export_venues/$', 'django_tablib.views.export', {
            'model': Venue,
            }),
    (r'^export_locations/$', 'django_tablib.views.export', {
            'model': Location,
            }),
)


