from django.db import models
from datetime import datetime
from django.template.defaultfilters import date as _date

class Person(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    nick_name = models.CharField(max_length=40)
    date_of_birth = models.DateField()#widget=DateInput(format='%d-%m-%y'), input_formats=('%d-%m-%y'))

    def __unicode__(self):
        name = [self.first_name, self.last_name]
        
        if self.nick_name:
            return (" '%s' " % self.nick_name).join(name) 

        return " ".join(name)

class Manager(Person):
    pass

class Musician(Person):
    instrument = models.CharField(max_length=50)

class Owner(Person):
    # Not sure if this will be a thing yet. Just a placeholder
    pass

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __unicode__(self):
        return self.name

class Band(models.Model):
    name = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre)
    members = models.ManyToManyField(Musician, through='BandMembership')

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

class Location(models.Model):
    # this will be replaced with geodjango
    street_address = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    suburb = models.CharField(max_length=150)
    post_code  = models.CharField(max_length=150)
    lat = models.DecimalField(max_digits=12, decimal_places=6, verbose_name='latitude', blank=True, null=True)
    lon = models.DecimalField(max_digits=12, decimal_places=6, verbose_name='longitude', blank=True, null=True)
    
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

class Sibling(models.Model):
    name = models.CharField(max_length=50)

class Venue(models.Model):
    STATUS_CHOICES = (
            ('O', 'Open'),
            ('C', 'Closed'),
            )
    #uid = models.CharField(max_length=5, unique=True)
    uid = models.CharField(max_length=5)
    name = models.CharField(max_length=50, default='Unnamed Venue')
    location = models.ForeignKey(Location, blank=True, null=True)
    stages = models.ManyToManyField(Stage, blank=True)
    venue_type = models.CharField(max_length=50, blank=True)# TODO: make this a set list or fk
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True)
    status_notes = models.CharField(max_length=300, blank=True)
    comment = models.CharField(max_length=300, blank=True)
    sibling = models.ManyToManyField(Sibling)


    def __unicode__(self):
        return self.name

class Gig(models.Model):

    start = models.DateTimeField(default=datetime.now)
    finish = models.DateTimeField(default=datetime.now)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    name  = models.CharField(max_length=150, blank=True)
    #cost = models.FloatField(blank=True)
    comment = models.CharField(max_length=300, blank=True)

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
            name += " on %s " % _date(self.start.date(), "l, M j, o")
    
        if not name:
            name = "No bands and no venue specified"
        return name
