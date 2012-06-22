from gigs.gig_registry.models import Gig
from haystack.indexes import SearchIndex, CharField
from haystack import site

class GigIndex(SearchIndex):
    text = CharField(document=True)#, use_template=True)

    def get_model(self):
        return Gig

    def index_queryset(self):
        return self.get_model().objects.all()

site.register(Gig, GigIndex)
