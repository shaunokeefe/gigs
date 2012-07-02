
from django.contrib import admin
from gigs.search import models

class SearchQueryRecordAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'time', 'result_count')
    search_fields = ('query', 'user__username')

admin.site.register(models.SearchQueryRecord, SearchQueryRecordAdmin)
