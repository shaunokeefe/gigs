# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('gig_registry_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('nick_name', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('gig_registry', ['Person'])

        # Adding model 'Manager'
        db.create_table('gig_registry_manager', (
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gig_registry.Person'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('gig_registry', ['Manager'])

        # Adding model 'Musician'
        db.create_table('gig_registry_musician', (
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gig_registry.Person'], unique=True, primary_key=True)),
            ('instrument', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('gig_registry', ['Musician'])

        # Adding model 'Owner'
        db.create_table('gig_registry_owner', (
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gig_registry.Person'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('gig_registry', ['Owner'])

        # Adding model 'Genre'
        db.create_table('gig_registry_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('gig_registry', ['Genre'])

        # Adding model 'Band'
        db.create_table('gig_registry_band', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('founded', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('gig_registry', ['Band'])

        # Adding M2M table for field genre on 'Band'
        db.create_table('gig_registry_band_genre', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('band', models.ForeignKey(orm['gig_registry.band'], null=False)),
            ('genre', models.ForeignKey(orm['gig_registry.genre'], null=False))
        ))
        db.create_unique('gig_registry_band_genre', ['band_id', 'genre_id'])

        # Adding model 'BandMembership'
        db.create_table('gig_registry_bandmembership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('started', self.gf('django.db.models.fields.DateField')()),
            ('finished', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gig_registry.Band'])),
            ('musician', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gig_registry.Musician'])),
        ))
        db.send_create_signal('gig_registry', ['BandMembership'])

        # Adding model 'Location'
        db.create_table('gig_registry_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('suburb', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('post_code', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=6, blank=True)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=6, blank=True)),
        ))
        db.send_create_signal('gig_registry', ['Location'])

        # Adding model 'Stage'
        db.create_table('gig_registry_stage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('gig_registry', ['Stage'])

        # Adding model 'Venue'
        db.create_table('gig_registry_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gig_registry.Location'])),
            ('established', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('venue_type', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='O', max_length=1)),
            ('status_notes', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('gig_registry', ['Venue'])

        # Adding M2M table for field stages on 'Venue'
        db.create_table('gig_registry_venue_stages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('venue', models.ForeignKey(orm['gig_registry.venue'], null=False)),
            ('stage', models.ForeignKey(orm['gig_registry.stage'], null=False))
        ))
        db.create_unique('gig_registry_venue_stages', ['venue_id', 'stage_id'])

        # Adding model 'Gig'
        db.create_table('gig_registry_gig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('finish', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gig_registry.Venue'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('cost', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('gig_registry', ['Gig'])

        # Adding M2M table for field bands on 'Gig'
        db.create_table('gig_registry_gig_bands', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gig', models.ForeignKey(orm['gig_registry.gig'], null=False)),
            ('band', models.ForeignKey(orm['gig_registry.band'], null=False))
        ))
        db.create_unique('gig_registry_gig_bands', ['gig_id', 'band_id'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table('gig_registry_person')

        # Deleting model 'Manager'
        db.delete_table('gig_registry_manager')

        # Deleting model 'Musician'
        db.delete_table('gig_registry_musician')

        # Deleting model 'Owner'
        db.delete_table('gig_registry_owner')

        # Deleting model 'Genre'
        db.delete_table('gig_registry_genre')

        # Deleting model 'Band'
        db.delete_table('gig_registry_band')

        # Removing M2M table for field genre on 'Band'
        db.delete_table('gig_registry_band_genre')

        # Deleting model 'BandMembership'
        db.delete_table('gig_registry_bandmembership')

        # Deleting model 'Location'
        db.delete_table('gig_registry_location')

        # Deleting model 'Stage'
        db.delete_table('gig_registry_stage')

        # Deleting model 'Venue'
        db.delete_table('gig_registry_venue')

        # Removing M2M table for field stages on 'Venue'
        db.delete_table('gig_registry_venue_stages')

        # Deleting model 'Gig'
        db.delete_table('gig_registry_gig')

        # Removing M2M table for field bands on 'Gig'
        db.delete_table('gig_registry_gig_bands')


    models = {
        'gig_registry.band': {
            'Meta': {'object_name': 'Band'},
            'founded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gig_registry.Genre']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gig_registry.Musician']", 'null': 'True', 'through': "orm['gig_registry.BandMembership']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'finish': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gig_registry.Venue']"})
        },
        'gig_registry.location': {
            'Meta': {'object_name': 'Location'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '6', 'blank': 'True'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '6', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'suburb': ('django.db.models.fields.CharField', [], {'max_length': '150'})
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
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'nick_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
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
            'venue_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['gig_registry']