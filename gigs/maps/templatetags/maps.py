from django import template
from django import forms
from gmapi.forms.widgets import GoogleMap
from gmapi import maps

from gigs.gig_registry.models import Location, Gig


class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))
    

class GigSearchMapNode(template.Node):
    def __init__(self, gigs):
        self.gigs = template.Variable(gigs)
    
    def render(self, context):
        try:
            gigs = self.gigs.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        
        lat = -37.809018
        lon = 144.963635
        gmap = maps.Map(opts = {
            'center': maps.LatLng(lat, lon),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 8,
            'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DROPDOWN_MENU
                },
            })
        
        for gig_search_result in gigs:
            gig = gig_search_result.object
            if gig.venue and  gig.venue.location:
                lat = gig.venue.location.lat
                lon = gig.venue.location.lon
                marker = maps.Marker(opts = {
                    'map': gmap,
                    'position': maps.LatLng(lat, lon),
                    })
                info = maps.InfoWindow({
                            'content': "gig location",
                            'disableAutoPan': True
                                        })
                info.open(gmap, marker)
                context['form'] = MapForm(initial={'map':gmap})
        return ''

class GigMapNode(template.Node):
    
    def __init__(self, gig):
        self.gig = template.Variable(gig)
   
    def render(self, context):
        try:
            gigs = self.gig.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if isinstance(gigs, Gig):
            gigs = [gigs]

        lat = -37.809018
        lon = 144.963635
        gmap = maps.Map(opts = {
            'center': maps.LatLng(lat, lon),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 10,
            'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DROPDOWN_MENU
                },
            })

        for gig in gigs:
            if gig.venue and  gig.venue.location:
                lat = gig.venue.location.lat
                lon = gig.venue.location.lon
                marker = maps.Marker(opts = {
                    'map': gmap,
                    'position': maps.LatLng(lat, lon),
                    })
        context['form'] = MapForm(initial={'map':gmap})
        return ''
        
def do_gig_map(parser, token):

    try:
        tag_name, gig, search_results = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires 2 arguments' % 
                token.contents.split()[0])
    if search_results == "search":
        return GigSearchMapNode(gig)
    return GigMapNode(gig)

class BandMapNode(template.Node):

    def __init__(self, band):
        self.band = template.Variable(band)

    def render(self, context):
        try:
            band = self.band.resolve(context)
        except template.VariableDoesNotExist:
            return ''
      
        # TODO how to get this?
        # Currently we're just on Swanston St.
        lat = -37.809018
        lon = 144.963635
        gmap = maps.Map(opts = {
            'center': maps.LatLng(lat, lon),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 8,
            'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DROPDOWN_MENU
                },
            })

        for location in Location.objects.for_band(band):
            lat = location.lat
            lon = location.lon
            
            marker = maps.Marker(opts = {
                'map': gmap,
                'position': maps.LatLng(lat, lon),
                })
            info = maps.InfoWindow({
                        'content': "gig location",
                        'disableAutoPan': True
                                    })
            info.open(gmap, marker)
        context['form'] = MapForm(initial={'map':gmap})
        return ''
        
def do_band_map(parser, token):

    try:
        tag_name, band = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires 1 argument' % 
                token.contents.split()[0])

    return BandMapNode(band)
 

class VenueMapNode(template.Node):

    def __init__(self, venue):
        self.venue = template.Variable(venue)

    def render(self, context):
        try:
            venue = self.venue.resolve(context)
        except template.VariableDoesNotExist:
            return ''
      
        # TODO how to get this?
        # Currently we're just on Swanston St.
        lat = -37.809018
        lon = 144.963635
        gmap = maps.Map(opts = {
            'center': maps.LatLng(lat, lon),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 8,
            'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DROPDOWN_MENU
                },
            })

        for location in Location.objects.for_venue(venue):
            lat = location.lat
            lon = location.lon
            
            marker = maps.Marker(opts = {
                'map': gmap,
                'position': maps.LatLng(lat, lon),
                })
            info = maps.InfoWindow({
                        'content': "gig location",
                        'disableAutoPan': True
                                    })
            info.open(gmap, marker)
        context['form'] = MapForm(initial={'map':gmap})
        return ''
        
def do_venue_map(parser, token):

    try:
        tag_name, venue = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires 1 argument' % 
                token.contents.split()[0])

    return VenueMapNode(venue)

register = template.Library()
register.tag('gig_map', do_gig_map)
register.tag('band_map', do_band_map)
register.tag('venue_map', do_venue_map)
