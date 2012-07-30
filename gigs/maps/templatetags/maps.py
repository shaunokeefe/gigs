from django import template
from django import forms
from gmapi.forms.widgets import GoogleMap
from gmapi import maps

from gigs.gig_registry.models import Location


class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))
    

class GigMapNode(template.Node):
    def __init__(self, gig):
        self.gig = template.Variable(gig)
    def render(self, context):
        try:
            gig = self.gig.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        lat = gig.venue.location.lat
        lon = gig.venue.location.lon
        gmap = maps.Map(opts = {
            'center': maps.LatLng(lat, lon),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 15,
            'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DROPDOWN_MENU
                },
            })
        marker = maps.Marker(opts = {
            'map': gmap,
            'position': maps.LatLng(lat, lon),
            })
        context['form'] = MapForm(initial={'map':gmap})
        return ''
        
def do_gig_map(parser, token):

    try:
        tag_name, gig = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires 1 argument' % 
                token.contents.split()[0])

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
 


register = template.Library()
register.tag('gig_map', do_gig_map)
register.tag('band_map', do_band_map)


