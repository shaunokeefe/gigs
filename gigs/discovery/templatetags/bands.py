from django import template
from django.template.loader import render_to_string
from django.conf import settings

from gigs.gig_registry import models as gig_registry_models

register = template.Library()

@register.simple_tag
def bands_played_with(band, **kwargs):
    # band = kwargs.get('band', None)
    if not band or not isinstance(band, gig_registry_models.Band):
        return ''
    display_length = kwargs.get('display_length', 5)

    band_gigs = gig_registry_models.Gig.objects.filter(bands__pk=band.pk)
    gig_pks = [gig.pk for gig in band_gigs]
    related_bands = gig_registry_models.Band.objects.exclude(pk=band.pk).filter(gig__pk__in=gig_pks).order_by('?').distinct()
    related_bands_slice = related_bands[:display_length]
    rendered_string = render_to_string(
        'discovery/related_bands.html',
        {'band': band, 'bands': related_bands_slice}
    )
    return rendered_string
