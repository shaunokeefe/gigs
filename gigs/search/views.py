from haystack.views import SearchView
from gigs.search.models import SearchQueryRecord

class LoggedSearchView(SearchView):
    
    def __call__(self, request):
        response = super(LoggedSearchView, self).__call__(request)
        query = SearchQueryRecord(
                query = self.query,
                result_count = self.results.count()
                )
        if not request.user.is_anonymous():
            query.user = request.user 
        query.save()

        return response
        


