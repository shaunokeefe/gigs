from django.contrib import admin
#from django.db import models as django_models
#from django.forms.extras.widgets import SelectDateWidget
from gigs.gig_registry import models


class MusicianInline(admin.TabularInline):
    fields = ['musician', 'started', 'finished', 'date_of_birth', 'instrument',]
    #formfield_overrides = {
    #        django_models.DateField: {'widget': SelectDateWidget},
    #        }
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
            (None, {'fields': ['venue','bands']}),
            ('Dates', {'fields': ['start', 'finish']}),
        ]

    filter_horizontal = ('bands',)
    #inlines = [BandInline]#, TestInline]# VenueInline]
    list_filter = ('venue', 'bands',)

admin.site.register(models.Band, BandAdmin)
admin.site.register(models.Musician)#, MusicianAdmin)
admin.site.register(models.Owner)
admin.site.register(models.Venue)
admin.site.register(models.Location)
admin.site.register(models.Genre)
admin.site.register(models.Gig, GigAdmin)
admin.site.register(models.BandMembership, MembershipAdmin)
