# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Band.comment_txt'
        db.add_column('gig_registry_band', 'comment_txt',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=300, blank=True),
                      keep_default=False)

        # Adding field 'Venue.comment_txt'
        db.add_column('gig_registry_venue', 'comment_txt',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=300, blank=True),
                      keep_default=False)

        # Adding field 'Location.comment_txt'
        db.add_column('gig_registry_location', 'comment_txt',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=300, blank=True),
                      keep_default=False)

        # Adding field 'Person.comment_txt'
        db.add_column('gig_registry_person', 'comment_txt',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=300, blank=True),
                      keep_default=False)

        # Adding field 'Gig.comment_txt'
        db.add_column('gig_registry_gig', 'comment_txt',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=300, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Band.comment_txt'
        db.delete_column('gig_registry_band', 'comment_txt')

        # Deleting field 'Venue.comment_txt'
        db.delete_column('gig_registry_venue', 'comment_txt')

        # Deleting field 'Location.comment_txt'
        db.delete_column('gig_registry_location', 'comment_txt')

        # Deleting field 'Person.comment_txt'
        db.delete_column('gig_registry_person', 'comment_txt')

        # Deleting field 'Gig.comment_txt'
        db.delete_column('gig_registry_gig', 'comment_txt')


    models = {
        'gig_registry.band': {
            'Meta': {'object_name': 'Band'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'comment_txt': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'founded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gig_registry.Genre']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gig_registry.Musician']", 'null': 'True', 'through': "orm['gig_registry.BandMembership']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
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
            'comment_txt': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'finish': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'updated_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gig_registry.Venue']"})
        },
        'gig_registry.location': {
            'Meta': {'object_name': 'Location'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'comment_txt': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
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
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'comment_txt': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'nick_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
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
            'comment_txt': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'established': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gig_registry.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gig_registry.Stage']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'O'", 'max_length': '1'}),
            'status_notes': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'venue_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['gig_registry']