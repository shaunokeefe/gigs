from tastypie.resources import ModelResource
from gigs.gig_registry.models import Gig

class GigResource(ModelResource):
    class Meta:
        queryset = Gig.objects.all()
        resource_name = 'gig'
