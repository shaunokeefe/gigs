from django.db import models

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
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    suburb = models.CharField(max_length=150)
    post_code  = models.CharField(max_length=150)
    
    def __unicode__(self):
        return self.location

class Venue(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.name

class Gig(models.Model):
    start = models.DateTimeField()
    finish = models.DateTimeField()
    venue = models.ForeignKey(Venue)

    # TODO members can be absent on the night..is this a problem?
    # maybe an 'appearance' model or something like that?
    bands= models.ManyToManyField(Band)

    def __unicode__(self):
        print self.bands
        return ", ".join(map(str, self.bands.all())) + " @ " + self.venue.name


class Test(models.Model):
    a = models.CharField(max_length=50)
    b = models.CharField(max_length=50)
    gig = models.ForeignKey(Gig)
