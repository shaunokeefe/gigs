from gmapi.maps import Geocoder
from django.db.models.signals import pre_save
from django.dispatch import receiver

from gigs.gig_registry.models import Location

# TODO: condsider what happens when a CSV entry
#       that has been previously been auto-corrected
#       is reloaded. The entries won't match. Maybe
#       all this logic belongs in an object manager
#       rather than in a signal e.g. a call on the
#       manager which corrects a populated instance.
#       that can be called in this signal *and* 
#       on a populated, un-saved instance that we
#       want to compare with something that has 
#       been previously auto-saved.
#
#       Alternatively, this also kind of feels like
#       something that could be handled in a custom
#       forms 'clean' function...

addr_mappings = { 
#    'street_number': 'street_number',
    #'route': 'street_name',
    'locality': ('suburb', 'long_name'),
    'administrative_area_level_1': ('state', 'short_name'),
    'country': ('country', 'long_name'),
    'postal_code' : ('post_code','long_name'),
}

@receiver(pre_save, sender=Location) 
def generate_longlat(sender, **kwargs):
    geocoder = Geocoder()
    loc = kwargs['instance']

    if False:
        # check if the instance is being created
        if loc.pk and loc.lat and loc.lon:
            # It created previously and is now
            # just being updated

            # Check if the address has changed
            try:
                old_loc = sender.objects.get(pk=loc.pk)
                if  str(old_loc) == str(loc):
                    # the addresses havnt changed so there's
                    # no need to update the latlong
                    return
                if old_loc.lat != loc.lat or old_loc.lon != loc.lon:
                    # the latlong has been manually updated
                    # so we shouldn't change it
                    return
            except Location.DoesNotExist:
                # this doesnt make a lot of sense but...
                pass
    if loc.pk:
        # The location has already previously
        # been saved to the db and doesnt 
        # need to have fields auto filled
        return
    
    if not loc.street_address and not loc.suburb:
        # no suburb or address so we're not going to
        # get meaningful results
        return

    addr = str(loc)
    
    # See of google can find the address
    result, code = geocoder.geocode({'address':addr})

    if code != 'OK':
        # something went wrong...
        return

    # 'result' looks like:
    #   
    #   [{
    #       'geometry': {
    #           'location': {
    #               'arg': [-37.81928, 145.004793], 
    #               'cls': 'LatLng'
    #               }, 
    #           'viewport': {
    #               'arg': [
    #                   {
    #                       'arg': [-37.820629, 145.003444], 
    #                       'cls': 'LatLng'
    #                   }, 
    #                   {
    #                       'arg': [-37.817931, 145.006142], 
    #                       'cls': 'LatLng'
    #                   }
    #                   ], 
    #               'cls': 'LatLngBounds'
    #               }, 
    #           'location_type': 'ROOFTOP'
    #           }, 
    #       'address_components': [
    #           {
    #               'long_name': '400', 
    #               'types': ['street_number'], 
    #               'short_name': '400'
    #           }, 
    #           {'
    #               long_name': 'Bridge Rd', 
    #               'types': ['route'], 
    #               'short_name': 'Bridge Rd'
    #           }, 
    #           {
    #               'long_name': 'Richmond', 
    #               'types': ['locality', 'political'], 
    #               'short_name': 'Richmond'
    #           }, 
    #           {
    #               'long_name': 'Victoria', 
    #               'types': ['administrative_area_level_1', 'political'], 
    #               'short_name': 'VIC'
    #           }, 
    #           {
    #               'long_name': 'Australia', 
    #               'types': ['country', 'political'], 
    #               'short_name': 'AU'
    #           }, 
    #           {
    #               'long_name': '3121', 
    #               'types': ['postal_code'], 
    #               'short_name': '3121'
    #           }
    #           ], 
    #       'formatted_address': '400 Bridge Rd, Richmond VIC 3121, Australia', 
    #       'types': ['street_address']
    #       }]
    #
    # So like...just parse it?
    #
    
    entry = result[0]
    latitude, longitude = entry['geometry']['location']['arg'] 
    loc.lat = latitude
    loc.lon = longitude

    addr_components = entry['address_components']
   
    # match values returned from google to 
    # fields in our model
    for component in addr_components:
        for t in component['types']:
            [field_name, fmt] = addr_mappings.get(t, (None, None))
            if field_name and not loc.__getattribute__(field_name):
                # TODO make content safe
                loc.__setattr__(field_name, component[fmt])
