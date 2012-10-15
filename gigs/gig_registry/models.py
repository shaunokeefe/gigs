from django.db import models
from django.db.models.query import QuerySet
from django.template.defaultfilters import date as _date

class Note(models.Model):
    note_text = models.TextField()

    def __unicode(self):
        return self.note_text

class Person(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    nick_name = models.CharField(max_length=40, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    note = models.ManyToManyField(Note)

    def __unicode__(self):
        name = [self.first_name, self.last_name]

        if self.nick_name:
            return (" '%s' " % self.nick_name).join(name)

        return " ".join(name)

class Manager(Person):
    pass

class Musician(Person):
    instrument = models.CharField(max_length=50, blank=True)

class Owner(Person):
    # Not sure if this will be a thing yet. Just a placeholder
    pass

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

class Band(models.Model):
    name = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre, blank=True, null=True)
    members = models.ManyToManyField(Musician, through='BandMembership', blank=True, null=True)
    founded = models.DateField(blank=True, null=True)

    note = models.ManyToManyField(Note)

    def __unicode__(self):
        return self.name

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

class LocationManager(models.Manager):


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
    # this will be replaced with geodjango
    street_address = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    suburb = models.CharField(max_length=150)
    post_code  = models.CharField(max_length=150)
    lat = models.DecimalField(max_digits=12, decimal_places=6, verbose_name='latitude', blank=True, null=True)
    lon = models.DecimalField(max_digits=12, decimal_places=6, verbose_name='longitude', blank=True, null=True)

    note = models.ManyToManyField(Note)

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

class Venue(models.Model):
    STATUS_CHOICES = (
            ('O', 'Open'),
            ('C', 'Closed'),
            )
    uid = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location)
    established = models.IntegerField(blank=True, null=True)
    stages = models.ManyToManyField(Stage, blank=True, null=True)
    venue_type = models.CharField(max_length=50, blank=True)# TODO: make this a set list or fk
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='O')
    status_notes = models.CharField(max_length=300, blank=True)
    comment = models.CharField(max_length=300, blank=True)

    note = models.ManyToManyField(Note)

    def __unicode__(self):
        if self.name:
            return self.name
        return 'Unnamed venue'

class Gig(models.Model):

    start = models.DateField()
    finish = models.DateField(blank=True, null=True)
    venue = models.ForeignKey(Venue)
    name  = models.CharField(max_length=150, blank=True)
    cost = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=300, blank=True)

    note = models.ManyToManyField(Note)

    # TODO members can be absent on the night..is this a problem?
    # maybe an 'appearance' model or something like that?
    bands = models.ManyToManyField(Band)

    def __unicode__(self):
        if self.name:
            return self.name
        name = ""
        if self.bands.count():
            bands = self.bands.all()
            name = bands[0].name
            if bands.count() > 1:
                name += " and others"

        if self.venue:
            name +=  " @ " + self.venue.name

        if self.start:
            name += " on %s " % _date(self.start, "l, M j")

        if not name:
            name = "No bands and no venue specified"
        return name
