import datetime

from django.contrib import admin
from django import forms
from django.forms.extras import widgets
from django.contrib.admin.widgets import AdminDateWidget
from gigs.gig_registry import models
from django.contrib.contenttypes import generic

class DistantHistorySelectDateWidget(widgets.SelectDateWidget):
    def __init__(self, attrs=None, years=None, required=True):
        if not years:
            years = range(datetime.date.today().year, 1900, -1)

        super(DistantHistorySelectDateWidget, self).__init__(attrs, years, required)

class DropdownDateModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DropdownDateModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__ == AdminDateWidget:
                field.widget = DistantHistorySelectDateWidget()

class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'uid':('name',)}
    form = DropdownDateModelForm

class MusicianInline(admin.TabularInline):
    fields = ['musician', 'started', 'finished', 'date_of_birth', 'instrument',]
    model = models.Musician
    form = DropdownDateModelForm

class MembershipInline(admin.TabularInline):
    model = models.BandMembership
    verbose_name = "Band Member"
    verbose_name_plural = "Band Members"
    fields = ['musician', 'started', 'finished']
    form = DropdownDateModelForm

    extra = 3

class BandAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]
    form = DropdownDateModelForm

class BandInline(admin.TabularInline):
    model = models.Gig.bands.through
    form = DropdownDateModelForm

class GigAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields': ['name', 'venue','bands', 'cost']}),
            ('Dates', {'fields': ['start', 'finish']}),
            ('Meta', {'fields': ['comment']}),
        ]

    filter_horizontal = ('bands',)
    list_filter = ('venue', 'bands',)
    form = DropdownDateModelForm

class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']

class LocationAdmin(admin.ModelAdmin):
    #fields = ['street_address', 'suburb', 'state', 'post_code', 'country', 'lat', 'lon']
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
            )
        ]

admin.site.register(models.Band, BandAdmin)
admin.site.register(models.Musician)
admin.site.register(models.Owner)
admin.site.register(models.Venue, VenueAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Gig, GigAdmin)
