from django.conf.urls.defaults import *
from haystack.query import SearchQuerySet
from gigs.search.forms import FacetedAllSearchForm
from gigs.search.views import LoggedSearchView, ajax_search_view

sqs = SearchQuerySet().facet('venue_name').facet('name')

urlpatterns = patterns(
    'search.views.',
    url(r'^$', LoggedSearchView(searchqueryset=sqs, form_class=FacetedAllSearchForm), name='index'),
    url(r'^search_ajax/$', ajax_search_view, name='search_ajax'),
)
