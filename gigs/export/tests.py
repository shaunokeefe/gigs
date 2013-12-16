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
        for v in topping1_values[0]:
            self.assertIn(v, pizza_values[0])
        for v in topping2_values[0]:
            self.assertIn(v, pizza_values[0])

class GigResourceTest(TestCase):

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

    def test_header_length(self):
        # Check headers are the same length as what comes out of export
        resource = GigResource()
        headers = resource.get_export_headers()
        rs = resource.get_export_headers()
        gig = Gig.objects.filter(pk=self.gig1.pk)
        exported_data = resource.export(gig)
        self.assertEqual(len(headers), (exported_data.width))

        gig = Gig.objects.filter(pk=self.gig2.pk)
        exported_data = resource.export(gig)
        self.assertEqual(len(headers), (exported_data.width))

    def test_bands(self):
        resource = GigResource()
        headers = resource.get_export_headers()
        gig = Gig.objects.filter(pk=self.gig1.pk)
        exported_data = resource.export(gig)

        self.assertTrue('bands.0.name' in headers)
        band1_name_column = headers.index('bands.0.name')
        band1_name = exported_data[0][band1_name_column]
        self.assertEqual(band1_name, self.band1.name)

        self.assertTrue('bands.1.name' in headers)
        band2_name_column = headers.index('bands.1.name')
        band2_name = exported_data[0][band2_name_column]
        self.assertEqual(band2_name, self.band2.name)

        self.assertFalse('bands.2.name' in headers)

        gig = Gig.objects.filter(pk=self.gig2.pk)
        exported_data = resource.export(gig)

        band1_name_column = headers.index('bands.0.name')
        band1_name = exported_data[0][band1_name_column]
        self.assertEqual(band1_name, self.band3.name)
