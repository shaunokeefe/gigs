from gigs.gig_registry.models import Gig
from haystack.indexes import RealTimeSearchIndex, \
    CharField, DateField, FloatField, MultiValueField
from haystack import site

class GigIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    tmp = CharField()
    start = DateField(model_attr='start', faceted=True)
    venue_name = CharField(model_attr='venue__name', faceted=True)
    bands = MultiValueField(faceted=True)
    band_members = MultiValueField(faceted=True)
    cost = FloatField(model_attr='cost', default=0)
    name = CharField(model_attr='name', default=0, faceted=True)
    venue_location = CharField(faceted=True)
    venue_status = CharField(model_attr='venue__status', faceted=True)
    venue_type = CharField(model_attr='venue__venue_type', faceted=True)
    venue_suburb = CharField(model_attr='venue__location__suburb', faceted=True)
    venue_postcode = CharField(model_attr='venue__location__post_code', faceted=True)

    def prepare_bands(self, obj):
        return [band.name for band in obj.bands.all()]

    def prepare_band_members(self, obj):
        members = []
        for band in obj.bands.all():
            members.extend([str(member) for member in band.members.all()])
        return members

    def prepare_location(self, obj):
        return str(obj.venue.location)

    def prepare_tmp(self, obj):
        return 'tmp'

    def index_queryset(self):
        return Gig.objects.all()


site.register(Gig, GigIndex)
