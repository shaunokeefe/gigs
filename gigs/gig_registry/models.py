from django.db import models
from django.db.models.query import QuerySet
from django.template.defaultfilters import date as _date
from django.contrib import auth
from django.core.urlresolvers import reverse

import datetime


class SourceType(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=40)
    author = models.CharField(max_length=100, blank=True, null=True)
    published = models.DateField()
    added_by = models.ForeignKey(auth.models.User, blank=True, null=True)
    source_type = models.ForeignKey(SourceType, blank=True, null=True)

    class Meta:
        unique_together = ('name', 'published')

    def __unicode__(self):
        rep = "%s, %s" % (self.name, self.published)
        if self.source_type:
            rep = rep + " (%s)" % (self.source_type)
        return rep

class UUIDManager(models.Manager):
    prefix = ''
    numbers_length = 7
    def get_next_UUID(self):
        next_number = 0
        for item in self.get_query_set().all().order_by('-uuid'):
            if not item.uuid:
                continue
            numeric_substring = item.uuid[1:]
            try:
                next_number = int(numeric_substring) + 1
                if next_number >= 10 ** (self.numbers_length -1):
                    continue
                break
            except ValueError:
                pass
        return "%s%s" % (self.prefix, str(next_number).zfill(self.numbers_length))

class GigUUIDManager(UUIDManager):
    prefix = 'G'

class PersonUUIDManager(UUIDManager):
    prefix = 'P'

class BandUUIDManager(UUIDManager):
    prefix = 'B'

class LocationUUIDManager(UUIDManager):
    prefix = 'L'

class VenueUUIDManager(UUIDManager):
    prefix = 'V'

class Person(models.Model):
    uuid = models.CharField(max_length=40, unique=True)
    created_at = models.DateField(default=datetime.date.today)
    updated_at = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    nick_name = models.CharField(max_length=40, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    comment = models.TextField(max_length=300, blank=True)


    def __unicode__(self):
        name = [self.first_name, self.last_name]

        if self.nick_name:
            return (" '%s' " % self.nick_name).join(name)

        return " ".join(name)

class Manager(Person):
    pass

class Musician(Person):
    instrument = models.CharField(max_length=50, blank=True)
    objects = PersonUUIDManager()

class Owner(Person):
    # Not sure if this will be a thing yet. Just a placeholder
    pass

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

class Band(models.Model):
    uuid = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateField(default=datetime.date.today)
    updated_at = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre, blank=True, null=True)
    members = models.ManyToManyField(Musician, through='BandMembership', blank=True, null=True)
    founded = models.DateField(blank=True, null=True)
    comment = models.TextField(max_length=300, blank=True)

    objects = BandUUIDManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portal_band_detail', args=[str(self.id)])

class BandMembership(models.Model):
    started = models.DateField()
    finished = models.DateField(blank=True, null=True)
    band = models.ForeignKey(Band)
    musician = models.ForeignKey(Musician)

    def __unicode__(self):
        return '%s in %s (%s to %s)' % (
                    self.musician,
                    self.band ,
                    self.started,
                    self.finished if self.finished else 'present')

class LocationManager(LocationUUIDManager):


    def _filter_instance_or_queryset(self, field, instances):
        if isinstance(instances, (QuerySet, list,)):
            field += '__in'
        filter_set = {field: instances}
        return Location.objects.filter(**filter_set).distinct()

    def for_bands(self, band):
        return self._filter_instance_or_queryset('venue__gig__bands', band)

    def for_venues(self, venue):
        return self._filter_instance_or_queryset('venue', venue)

    def for_gigs(self, gigs):
        return self._filter_instance_or_queryset('venue__gig', gigs)

class Location(models.Model):
    uuid = models.CharField(max_length=40, unique=True)
    created_at = models.DateField(default=datetime.date.today)
    updated_at = models.DateField(blank=True, null=True)
    # this will be replaced with geodjango
    building_name = models.CharField(max_length=150, blank=True, null=True)
    street_address = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    suburb = models.CharField(max_length=150)
    post_code  = models.CharField(max_length=150)
    comment = models.TextField(max_length=300, blank=True)
    lat = models.DecimalField(max_digits=12, decimal_places=6, verbose_name='latitude', blank=True, null=True)
    lon = models.DecimalField(max_digits=12, decimal_places=6, verbose_name='longitude', blank=True, null=True)

    objects = LocationManager()

    def __unicode__(self):
        return "%s, %s %s, %s %s" % (
                self.street_address,
                self.suburb,
                self.state,
                self.post_code,
                self.country
                )

class Stage(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.name

class Venue(models.Model):
    STATUS_CHOICES = (
            ('O', 'Open'),
            ('C', 'Closed'),
            )
    uuid = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location)
    established = models.IntegerField(blank=True, null=True)
    stages = models.ManyToManyField(Stage, blank=True, null=True)
    venue_type = models.CharField(max_length=50, blank=True)# TODO: make this a set list or fk
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='O')
    status_notes = models.CharField(max_length=300, blank=True)
    comment = models.TextField(max_length=300, blank=True)

    objects = VenueUUIDManager()

    def __unicode__(self):
        if self.name:
            return self.name
        return 'Unnamed venue'

class GigType(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return self.name

#class GigUUIDManager(models.Manager):
#    def get_next_UUID(self):
#        max_uuid = self.get_query_set().all().order_by('-uuid')[0].uuid
#        next_number = int(max_uuid[1:]) + 1
#        return "G%s" % (str(next_number).zfill(7))


class Gig(models.Model):

    uuid = models.CharField(max_length=40, unique=True)
    created_at = models.DateField(default=datetime.date.today)
    updated_at = models.DateField(blank=True, null=True)
    start = models.DateField()
    finish = models.DateField(blank=True, null=True)
    venue = models.ForeignKey(Venue)
    name  = models.CharField(max_length=150, blank=True)
    cost = models.FloatField(blank=True, null=True)
    gig_type = models.ForeignKey(GigType, blank=True, null=True)
    comment = models.TextField(max_length=300, blank=True)
    source = models.ForeignKey(Source, blank=True, null=True)

    # TODO members can be absent on the night..is this a problem?
    # maybe an 'appearance' model or something like that?
    bands = models.ManyToManyField(Band, through='Performance')

    objects = GigUUIDManager()

    def __unicode__(self):
        if self.name:
            return self.name
        name = ""
        if self.bands.count():
            name = ', '.join([band.name for band in self.get_headlining_bands()])
            if self.get_non_headlining_bands():
                name += " and others"

        if self.venue:
            name +=  " @ " + self.venue.name

        if self.start:
            name += " on %s " % _date(self.start, "l, M j Y")

        if not name:
            name = "No bands and no venue specified"
        return name

    def get_headlining_bands(self):
        return self.bands.filter(performance__order=Performance.HEADLINER)

    def get_non_headlining_bands(self):
        return [p.band for p in Performance.objects.\
                exclude(order=Performance.HEADLINER).\
                filter(gig=self).order_by('order')]


class Performance(models.Model):
    HEADLINER       = 1
    FIRST_SUPPORT   = 2
    SECOND_SUPPORT  = 3
    THIRD_SUPPORT   = 4
    FOURTH_SUPPORT  = 5
    FIFTH_SUPPORT   = 6
    SIXTH_SUPPORT   = 7
    SEVENTH_SUPPORT = 8
    EIGTH_SUPPORT   = 9
    NINTH_SUPPORT   = 10
    TENTH_SUPPORT   = 11

    ORDER_CHOICES = (
            (HEADLINER, 'Headliner'),
            (FIRST_SUPPORT, 'First support'),
            (SECOND_SUPPORT, 'Second support'),
            (THIRD_SUPPORT, 'Third support'),
            (FOURTH_SUPPORT, 'Fourth support'),
            (FIFTH_SUPPORT, 'Fifth support'),
            (SIXTH_SUPPORT, 'Sixth support'),
            (SEVENTH_SUPPORT, 'Seventh support'),
            (EIGTH_SUPPORT, 'Eigth support'),
            (NINTH_SUPPORT, 'Ninth support'),
            (TENTH_SUPPORT, 'Tenth support'),
            )
    band = models.ForeignKey(Band)
    gig = models.ForeignKey(Gig)
    order = models.IntegerField(choices=ORDER_CHOICES, default=1)
    time = models.TimeField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, blank=True, null=True)
    stage = models.ForeignKey(Stage, null=True, blank=True)
