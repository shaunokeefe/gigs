from django.contrib import admin
#from django.db import models as django_models
#from django.forms.extras.widgets import SelectDateWidget
from gigs.gig_registry import models


class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'uid':('name',)}

class MusicianInline(admin.TabularInline):
    fields = ['musician', 'started', 'finished', 'date_of_birth', 'instrument',]
    model = models.Musician

#class MusicianAdmin(admin.ModelAdmin):
#    inlines = [MembershipInline]

class MembershipAdmin(admin.ModelAdmin):
    pass#inlines = [MusicianInline]

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
            ('Meta', {'fields': ['comment']}),
        ]
    
    filter_horizontal = ('bands',)
    list_filter = ('venue', 'bands',)

class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']

class LocationAdmin(admin.ModelAdmin):
    fields = ['street_address', 'suburb', 'state', 'post_code', 'country', 'lat', 'lon']

admin.site.register(models.Band, BandAdmin)
admin.site.register(models.Musician)
admin.site.register(models.Owner)
admin.site.register(models.Venue, VenueAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Gig, GigAdmin)
admin.site.register(models.BandMembership, MembershipAdmin)
