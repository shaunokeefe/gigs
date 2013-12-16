from django.db.models import Count, Max
from import_export.resources import ModelResource
from import_export.fields import Field

from gigs.gig_registry.models import Gig, Band, Venue, Location
from gigs.export.widgets import FollowManyToManyWidget
from gigs.export.fields import RelatedM2MResourceField

class FollowModelResource(ModelResource):
    """Handle multiple return values from export_field
    """

    def get_export_headers(self):

        headers = []
        for field in self.get_fields():
            if isinstance(field, RelatedM2MResourceField):
                sub_headers = field.related_resource.get_export_headers()
                count = self._meta.model.objects.all().annotate(num=Count(field.column_name)).aggregate(max=Max('num'))['max']
                formatted_headers = []
                for i in range(count):
                    for header in sub_headers:
                        formatted_headers.append("%s.%d.%s" % (field.column_name, i, header))
                headers.extend(formatted_headers)

            else:
                headers.append(field.column_name)
        return headers

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

    # TODO (shauno): could try setting column_name as a descriptor
    # which returns a list of headers for all the band fields
