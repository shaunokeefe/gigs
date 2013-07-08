from django.contrib import admin
from django_tablib.admin import TablibAdmin
from django import forms

from gigs.gig_registry import models

class AutofillUUIDForm(forms.ModelForm):
    class Meta:
        model = None
    def __init__(self, *args, **kwargs):
        # TODO(shauno): This method stops working once we have multiple
        # users adding gigs at the same time. Two users pull up the same
        # form and they will get the same UUID, and the first one to
        # submit gets to use it, the second one will not be able to submit
        # their form because the UUID is not unique. Might be better to
        # generate on save, but this is an implicit action, and may not
        # be intuitive for the user
        #
        print args
        print kwargs
        if not kwargs.get('instance', None):
            if not kwargs.get('initial', None):
                kwargs['initial'] = {}
            kwargs['initial'].update({'uuid': self.Meta.model.objects.get_next_UUID()})
        super(AutofillUUIDForm, self).__init__(*args, **kwargs)



class MusicianAutofillUUIDForm(AutofillUUIDForm):
    class Meta:
        model = models.Musician

class MusicianAdmin(admin.ModelAdmin):
    form = MusicianAutofillUUIDForm

class MusicianInline(admin.TabularInline):
    form = MusicianAutofillUUIDForm
    fields = ['musician', 'started', 'finished', 'date_of_birth', 'instrument',]
    model = models.Musician

class MembershipInline(admin.TabularInline):
    model = models.BandMembership
    verbose_name = "Band Member"
    verbose_name_plural = "Band Members"
    fields = ['musician', 'started', 'finished']

    extra = 3

class BandAutofillUUIDForm(AutofillUUIDForm):
    class Meta:
        model = models.Band

class BandAdmin(admin.ModelAdmin):
    form = BandAutofillUUIDForm
    inlines = [MembershipInline]
    list_display = ['name']
    search_fields = ['name', 'comment']

class BandInline(admin.TabularInline):
    model = models.Gig.bands.through
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # limit the choice of stages to stages listed
        # for the gig's venue
        if db_field.name == "stage":
            try:
                gig = request.gig
                kwargs["queryset"] = models.Stage.objects.filter(venue__exact=gig.venue)
            except AttributeError:
                pass
        return super(BandInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

def get_venue_id(gig):
    return gig.venue.id

class GigAutofillUUIDForm(AutofillUUIDForm):
    class Meta:
        model = models.Gig

class GigAdmin(TablibAdmin):
    form =  GigAutofillUUIDForm
    fieldsets = [
            (None, {'fields': ['name', 'venue', 'cost', 'gig_type', 'source']}),
            ('Dates', {'fields': ['start', 'finish']}),
            ('Metadata', {'fields': ['uuid','comment']}),
        ]
    formats = ['csv', 'xls']
    headers = {
        'name': 'name',
        'start': 'start',
        'finish': 'finish',
        'cost': 'cost',
        'comment': 'comment',
        'venue.id': get_venue_id,
    }

    inlines = (BandInline,)

    list_filter = ('venue', 'bands',)
    search_fields = ['name', 'venue__name', 'comment']

    def get_form(self, request, obj=None, **kwargs):
        # add the gig object to the request so that it
        # can be passed down to the inlines. The inlines
        # use the object to limit the chocies in drop-
        # downs to relevant choices
        request.gig = obj
        return super(GigAdmin, self).get_form(request, obj, **kwargs)

    def get_gig_type(obj):
        return "%s" % (obj.gig_type.name)
    get_gig_type.short_description = 'Gig type'
    get_gig_type.admin_order_field = 'gig_type__name'

    def get_venue_name(obj):
        return "%s" % (obj.venue.name)
    get_venue_name.short_description = 'Venue'
    get_venue_name.admin_order_field = 'venue__name'

    def get_gig(obj):
        return obj
    get_gig.short_description = 'Gig'
    get_gig.admin_order_field = 'id'

    list_display = [get_gig, get_venue_name, 'name', 'start', 'cost', get_gig_type]
    ordering = ['-id']


def get_location_id(venue):
    return venue.location.id

class VenueAutofillUUIDForm(AutofillUUIDForm):
    class Meta:
        model = models.Venue

class VenueAdmin(TablibAdmin):
    form = VenueAutofillUUIDForm

    list_display = ['name', 'location', 'established', 'venue_type', 'status']
    list_filter = ('venue_type', 'status', 'location__suburb')

    search_fields = ['name', 'venue_type', 'location__suburb', 'comment']

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

class LocationAutofillUUIDForm(AutofillUUIDForm):
    class Meta:
        model = models.Location

class LocationAdmin(TablibAdmin):
    form =  LocationAutofillUUIDForm
    list_display = ['street_address', 'building_name', 'suburb', 'state', 'post_code', 'lat', 'lon']
    list_filter = ('suburb', 'post_code', 'state', 'building_name')
    fieldsets = [
            ('Address',
                {'fields':
                    [
                        'building_name',
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
    search_fields = ['street_address', 'suburb', 'post_code', 'state', 'building_name', 'comment']

admin.site.register(models.Band, BandAdmin)
admin.site.register(models.Musician, MusicianAdmin)
admin.site.register(models.Owner)
admin.site.register(models.Venue, VenueAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Gig, GigAdmin)
admin.site.register(models.GigType)
admin.site.register(models.Source)
admin.site.register(models.SourceType)
admin.site.register(models.BandMembership)
admin.site.register(models.Stage)
