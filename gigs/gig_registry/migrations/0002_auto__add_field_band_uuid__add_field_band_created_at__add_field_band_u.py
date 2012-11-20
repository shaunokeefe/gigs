# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Band.uuid'
        db.add_column('gig_registry_band', 'uuid',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True),
                      keep_default=False)

        # Adding field 'Band.created_at'
        db.add_column('gig_registry_band', 'created_at',
                      self.gf('django.db.models.fields.DateField')(default=datetime.date.today),
                      keep_default=False)

        # Adding field 'Band.updated_at'
        db.add_column('gig_registry_band', 'updated_at',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Venue.uuid'
        db.add_column('gig_registry_venue', 'uuid',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True),
                      keep_default=False)

        # Adding field 'Location.uuid'
        db.add_column('gig_registry_location', 'uuid',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True),
                      keep_default=False)

        # Adding field 'Location.created_at'
        db.add_column('gig_registry_location', 'created_at',
                      self.gf('django.db.models.fields.DateField')(default=datetime.date.today),
                      keep_default=False)

        # Adding field 'Location.updated_at'
        db.add_column('gig_registry_location', 'updated_at',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.uuid'
        db.add_column('gig_registry_person', 'uuid',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True),
                      keep_default=False)

        # Adding field 'Person.created_at'
        db.add_column('gig_registry_person', 'created_at',
                      self.gf('django.db.models.fields.DateField')(default=datetime.date.today),
                      keep_default=False)

        # Adding field 'Person.updated_at'
        db.add_column('gig_registry_person', 'updated_at',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Gig.uuid'
        db.add_column('gig_registry_gig', 'uuid',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True),
                      keep_default=False)

        # Adding field 'Gig.created_at'
        db.add_column('gig_registry_gig', 'created_at',
                      self.gf('django.db.models.fields.DateField')(default=datetime.date.today),
                      keep_default=False)

        # Adding field 'Gig.updated_at'
        db.add_column('gig_registry_gig', 'updated_at',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Band.uuid'
        db.delete_column('gig_registry_band', 'uuid')

        # Deleting field 'Band.created_at'
        db.delete_column('gig_registry_band', 'created_at')

        # Deleting field 'Band.updated_at'
        db.delete_column('gig_registry_band', 'updated_at')

        # Deleting field 'Venue.uuid'
        db.delete_column('gig_registry_venue', 'uuid')

        # Deleting field 'Location.uuid'
        db.delete_column('gig_registry_location', 'uuid')

        # Deleting field 'Location.created_at'
        db.delete_column('gig_registry_location', 'created_at')

        # Deleting field 'Location.updated_at'
        db.delete_column('gig_registry_location', 'updated_at')

        # Deleting field 'Person.uuid'
        db.delete_column('gig_registry_person', 'uuid')

        # Deleting field 'Person.created_at'
        db.delete_column('gig_registry_person', 'created_at')

        # Deleting field 'Person.updated_at'
        db.delete_column('gig_registry_person', 'updated_at')

        # Deleting field 'Gig.uuid'
        db.delete_column('gig_registry_gig', 'uuid')

        # Deleting field 'Gig.created_at'
        db.delete_column('gig_registry_gig', 'created_at')

        # Deleting field 'Gig.updated_at'
        db.delete_column('gig_registry_gig', 'updated_at')


    models = {
        'gig_registry.band': {
            'Meta': {'object_name': 'Band'},
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'founded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gig_registry.Genre']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gig_registry.Musician']", 'null': 'True', 'through': "orm['gig_registry.BandMembership']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'gig_registry.bandmembership': {
            'Meta': {'object_name': 'BandMembership'},
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gig_registry.Band']"}),
            'finished': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'musician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gig_registry.Musician']"}),
            'started': ('django.db.models.fields.DateField', [], {})
        },
        'gig_registry.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'gig_registry.gig': {
            'Meta': {'object_name': 'Gig'},
            'bands': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gig_registry.Band']", 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'finish': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'updated_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gig_registry.Venue']"})
        },
        'gig_registry.location': {
            'Meta': {'object_name': 'Location'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '6', 'blank': 'True'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '6', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'suburb': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'updated_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'gig_registry.manager': {
            'Meta': {'object_name': 'Manager', '_ormbases': ['gig_registry.Person']},
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gig_registry.Person']", 'unique': 'True', 'primary_key': 'True'})
        },
        'gig_registry.musician': {
            'Meta': {'object_name': 'Musician', '_ormbases': ['gig_registry.Person']},
            'instrument': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gig_registry.Person']", 'unique': 'True', 'primary_key': 'True'})
        },
        'gig_registry.owner': {
            'Meta': {'object_name': 'Owner', '_ormbases': ['gig_registry.Person']},
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gig_registry.Person']", 'unique': 'True', 'primary_key': 'True'})
        },
        'gig_registry.person': {
            'Meta': {'object_name': 'Person'},
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'nick_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'gig_registry.stage': {
            'Meta': {'object_name': 'Stage'},
            'capacity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'gig_registry.venue': {
            'Meta': {'object_name': 'Venue'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'established': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gig_registry.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gig_registry.Stage']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'O'", 'max_length': '1'}),
            'status_notes': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'venue_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['gig_registry']