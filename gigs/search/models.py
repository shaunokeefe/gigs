from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class SearchQueryRecord(models.Model):
    query = models.CharField(max_length=200)
    user = models.ForeignKey(User, blank=True, null=True)
    time = models.DateTimeField(default=datetime.now)
    result_count = models.IntegerField()

    def __unicode__(self):
        username = 'Anonymous'
        if self.user:
            username = self.user

        return "%s (%s): '%s'" % (username, self.time.strftime("%x %X"), self.query)
