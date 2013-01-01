from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

class FacetedAllSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        self.selected_date_facets = kwargs.pop("selected_date_facets", [])
        super(FacetedAllSearchForm, self).__init__(*args, **kwargs)

    def no_query_found(self):
        if self.searchqueryset:
            return self.searchqueryset
        sqs =  SearchQuerySet()
        if self.load_all:
            sqs = sqs.load_all()
        return sqs

    def search(self):
        sqs = super(FacetedAllSearchForm, self).search()
        for facet in self.selected_date_facets:
            sqs = sqs.narrow(facet)
        return sqs
