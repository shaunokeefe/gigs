from django.conf.urls.defaults import *
from gigs.search.views import LoggedSearchView, ajax_search_view

urlpatterns = patterns(
    'search.views.',
    url(r'^$', LoggedSearchView(), name='index'),
    url(r'^search_ajax/$', ajax_search_view, name='search_ajax'),
)
