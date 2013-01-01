import datetime

from django.conf.urls.defaults import *

from haystack.query import SearchQuerySet

from gigs.search.forms import FacetedAllSearchForm
from gigs.search.views import LoggedSearchView, ajax_search_view

sqs = SearchQuerySet().facet('venue_name')\
        .facet('name')\
        .facet('bands')\
        .date_facet('start', start_date=datetime.date(1950,1,1), end_date=datetime.date.today(), gap_by='year')#date(1980,1,1), gap_by='year')

urlpatterns = patterns(
    'search.views.',
    url(r'^$', LoggedSearchView(searchqueryset=sqs, form_class=FacetedAllSearchForm), name='index'),
    url(r'^search_ajax/$', ajax_search_view, name='search_ajax'),
)
