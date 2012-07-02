from django.conf.urls.defaults import *
#from haystack.views import SearchView
from gigs.search.views import LoggedSearchView

urlpatterns = patterns(
    'search.views.',
    url(r'^$', LoggedSearchView(), name='search_view'),
)
