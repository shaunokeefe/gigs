from django.contrib import admin
from gigs.gig_registry import models
from django_tablib.admin import TablibAdmin


class MusicianInline(admin.TabularInline):
    fields = ['musician', 'started', 'finished', 'date_of_birth', 'instrument',]
    model = models.Musician

class MembershipInline(admin.TabularInline):
    model = models.BandMembership
    verbose_name = "Band Member"
    verbose_name_plural = "Band Members"
    fields = ['musician', 'started', 'finished']

    extra = 3

class BandAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]

class BandInline(admin.TabularInline):
    model = models.Gig.bands.through


def get_venue_id(gig):
    return gig.venue.id


class GigAdmin(TablibAdmin):
    fieldsets = [
            (None, {'fields': ['name', 'venue','bands', 'cost', 'gig_type', 'source']}),
            ('Dates', {'fields': ['start', 'finish']}),
            ('Metadata', {'fields': ['uuid','comment']}),
        ]
    formats = ['csv', 'xls']
    headers={
        'name': 'name',
        'start': 'start',
        'finish': 'finish',
        'cost': 'cost',
        'comment': 'comment',
        'venue.id': get_venue_id,
        }

    filter_horizontal = ('bands',)
    list_filter = ('venue', 'bands',)

def get_location_id(venue):
    return venue.location.id

class VenueAdmin(TablibAdmin):
    list_display = ['name', 'location']

    formats = ['csv', 'xls']
    headers={
        'name': 'name',
        'uid': 'uid',
        'location.id': get_location_id,
        'established': 'established',
        'venue_type':'venue_type',
        'status':'status',
        'status_notes':'status_notes',
        'comment':'comment',
        }

class LocationAdmin(TablibAdmin):
    fieldsets = [
            ('Address',
                {'fields':
                    [
                        'street_address',
                        'suburb',
                        'state',
                        'post_code',
                        'country',
                    ]
                }
            ),
            ('Co-ordinates',
                {'fields':
                    [
                        'lat',
                        'lon',
                    ]
                }
            ),
            ('Metadata',
                {'fields':
                    [
                        'uuid',
                        'comment',
                    ]
                }
            )
        ]

    formats = ['csv', 'xls']

admin.site.register(models.Band, BandAdmin)
admin.site.register(models.Musician)
admin.site.register(models.Owner)
admin.site.register(models.Venue, VenueAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Gig, GigAdmin)
admin.site.register(models.GigType)
admin.site.register(models.Source)
admin.site.register(models.SourceType)
admin.site.register(models.BandMembership)
