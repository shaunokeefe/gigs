from import_export.resources import ModelResource
from import_export.fields import Field

from gigs.gig_registry.models import Gig, Band, Venue, Location
from gigs.export.widgets import FollowManyToManyWidget
from gigs.export.fields import RelatedM2MResourceField

class FollowModelResource(ModelResource):
    """Handle multiple return values from export_field
    """

    def export_resource(self, obj):
        values = []
        for field in self.get_fields():
            field_values = self.export_field(field, obj)
            if isinstance(field_values, list):
                values.extend(field_values)
            else:
                values.append(field_values)
        return values

class BandResource(ModelResource):

    class Meta:
        model = Band

class VenueResource(ModelResource):

    class Meta:
        model = Venue


class LocationResource(ModelResource):

    class Meta:
        model = Location

class GigResource(FollowModelResource):

    start = Field(attribute='start')
    venue_name = Field(attribute='venue__name')
    bands = RelatedM2MResourceField(BandResource, attribute='bands')

    class Meta:
        model = Gig
