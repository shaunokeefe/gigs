from gmapi.maps import Geocoder

def generate_longlat(sender, **kwargs):
    geocoder = Geocoder()
    addr = sender.__unicode__()
    result, code = geocoder.geocode({'address':addr})

    if code != 'OK':
        return
