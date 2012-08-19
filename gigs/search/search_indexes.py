from gigs.gig_registry.models import Gig
from haystack.indexes import RealTimeSearchIndex, CharField
from haystack import site

class GigIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)

    def index_queryset(self):
        return Gig.objects.all()

site.register(Gig, GigIndex)
