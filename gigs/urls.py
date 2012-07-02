
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from gigs.portal import urls as portal_urls
from gigs.search import urls as search_urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'', include(portal_urls)),
    (r'^admin/', include(admin.site.urls)),
    (r'^search/', include(search_urls)),
)


