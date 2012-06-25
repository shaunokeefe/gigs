from gigs.gig_registry.models import Gig
from haystack.indexes import SearchIndex, CharField
from haystack import site

class GigIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

    def index_queryset(self):
        return Gig.objects.all()

site.register(Gig, GigIndex)
