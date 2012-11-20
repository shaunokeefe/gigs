from django.contrib import admin
from gigs.gig_registry import models


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


class GigAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields': ['name', 'venue','bands', 'cost']}),
            ('Dates', {'fields': ['start', 'finish']}),
            ('Meta', {'fields': ['uuid','comment']}),
        ]
    
    filter_horizontal = ('bands',)
    list_filter = ('venue', 'bands',)

class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']

class LocationAdmin(admin.ModelAdmin):
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
                    ]
                }
            )
        ]

admin.site.register(models.Band, BandAdmin)
admin.site.register(models.Musician)
admin.site.register(models.Owner)
admin.site.register(models.Venue, VenueAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Gig, GigAdmin)
admin.site.register(models.BandMembership)
