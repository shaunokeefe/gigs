from django.conf.urls.defaults import *
from gigs.gig_registry.api import GigResource

gig_resource = GigResource()

urlpatterns = patterns('',
                        url(r'', include(gig_resource.urls)),
                       )
