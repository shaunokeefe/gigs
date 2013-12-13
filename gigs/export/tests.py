"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import date, datetime

from django.test import TestCase
from django.db import models

from import_export.resources import ModelResource

from gigs.export.fields import RelatedForeignKeyResourceField, \
        RelatedM2MResourceField
from gigs.export.resources import GigResource, VenueResource, \
        LocationResource, BandResource, FollowModelResource
from gigs.gig_registry.models import Gig, Venue, Location, Band, \
        Performance


class Pizza(models.Model):
    name = models.CharField(max_length=64)
    toppings = models.ManyToManyField('Topping')

class TimePeriod(models.Model):
    start = models.DateField()
    end = models.DateField()
    voucher = models.ForeignKey('Voucher')
    pizza = models.ForeignKey('Pizza')

class Voucher(models.Model):
    percent = models.IntegerField()
    pizzas = models.ManyToManyField('Pizza', through='TimePeriod')

class Topping(models.Model):
    name = models.CharField(max_length=64)

class PizzaResource(ModelResource):
    class Meta:
        model = Pizza

class VoucherResource(ModelResource):
    class Meta:
        model = Voucher

class ToppingResource(ModelResource):
    class Meta:
        model = Topping

class M2MFieldTest(TestCase):

    def setUp(self):
        self.pizza = Pizza(name='Hawaiian')
        self.pizza.save()
        self.topping1 = Topping(name='Pineapple')
        self.topping1.save()
        self.topping2 = Topping(name='Ham')
        self.topping2.save()
        self.pizza.toppings.add(self.topping1, self.topping2)
        self.voucher = Voucher(percent=90)
        self.voucher.save()

        self.time_period = TimePeriod(voucher=self.voucher,
                pizza=self.pizza, start=date(1982, 8, 29),
                end=date(1982, 8, 30))
        self.time_period.save()

    def test_export(self):
        """
        """
        topping_field = RelatedM2MResourceField(ToppingResource, attribute='toppings')
        topping_values = topping_field.export(self.pizza)
        self.assertIn(self.topping1.name, topping_values)
        self.assertIn(self.topping2.name, topping_values)

    def test_through(self):
        pizza_field = RelatedM2MResourceField(PizzaResource, attribute='pizzas')
        pizza_values = pizza_field.export(self.voucher)
        self.assertIn(self.pizza.name, pizza_values)



class ExportM2MFieldTest(TestCase):

    def setUp(self):
        self.location = Location(street_address='The street address')
        self.location.save()

        self.venue = Venue(name='The Northcote Social Club', location=self.location)
        self.venue.save()

        self.gig1 = Gig.objects.create(name='Laneway', venue=self.venue, start=datetime.now())
        self.gig1.save()
        self.band1 = Band(name='The Drones')
        self.band1.save()
        self.band2 = Band(name='Chvrches')
        self.band2.save()
        performance = Performance.objects.create(band=self.band1, gig=self.gig1, order=Performance.HEADLINER)
        performance.save()
        performance = Performance.objects.create(band=self.band2, gig=self.gig1, order=Performance.FIRST_SUPPORT)
        performance.save()

        self.gig2 = Gig(name='Laneway2', venue=self.venue, start=datetime.now(), uuid='2')
        self.gig2.save()
        self.band3 = Band(name='Peter Coombe')
        self.band3.save()
        performance = Performance.objects.create(band=self.band3, gig=self.gig2, order=Performance.HEADLINER)
        performance.save()

    def test_bands(self):
        field = RelatedM2MResourceField(BandResource, attribute='bands')
        band_values = field.export(self.gig1)
        self.assertIn(self.band1.name, band_values)
        self.assertIn(self.band2.name, band_values)
        self.assertNotIn(self.band3.name, band_values)

    def test_venue(self):
        field = RelatedForeignKeyResourceField(VenueResource, attribute='venue')
        venue_values = field.export(self.gig1)
        self.assertIn(self.venue.name, venue_values)

    def test_location(self):
        field = RelatedForeignKeyResourceField(LocationResource, attribute='location')
        location_values = field.export(self.venue)
        self.assertIn(self.location.street_address, location_values)

class PizzaFollowResource(FollowModelResource):

    toppings = RelatedM2MResourceField(ToppingResource, attribute='toppings')

    class Meta:
        model = Pizza

class FollowModelResourceTest(TestCase):

    def setUp(self):
        self.pizza = Pizza(name='Hawaiian')
        self.pizza.save()
        self.topping1 = Topping(name='Pineapple')
        self.topping1.save()
        self.topping2 = Topping(name='Ham')
        self.topping2.save()
        self.pizza.toppings.add(self.topping1, self.topping2)
        self.voucher = Voucher(percent=90)
        self.voucher.save()

        self.time_period = TimePeriod(voucher=self.voucher,
                pizza=self.pizza, start=date(1982, 8, 29),
                end=date(1982, 8, 30))
        self.time_period.save()

    def test_export(self):

        pizza_resource = PizzaFollowResource()
        topping_resource = ToppingResource()

        pizza_values = pizza_resource.export(queryset=Pizza.objects.filter(pk=self.pizza.pk))
        topping1_values = topping_resource.export(queryset=Topping.objects.filter(pk=self.topping1.pk))
        topping2_values = topping_resource.export(queryset=Topping.objects.filter(pk=self.topping2.pk))

        for v in topping1_values + topping2_values:
            self.assertIn(v, pizza_values)
