from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import utc
from django.db.models.query import QuerySet
from pytils import dt
import datetime
#from main import util

# Create your models here.
class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)

class Mark(models.Model):
    CRITERIA = ((1, 'Criteria  One'), (2, 'Criteria Two'), (3, 'Criteria Three'), (4, 'Criteria Four'))
    from_user = models.ForeignKey(User, related_name='sent_marks')
    to_user = models.ForeignKey(User, related_name='received_marks')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    criterion = models.PositiveSmallIntegerField(choices=CRITERIA)
    value = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=40, blank=True)
    objects = QuerySetManager()

    class QuerySet(QuerySet):
        def get_actual(self, days=14):
            start = datetime.datetime.now()-datetime.timedelta(days)
            return self.filter(date__gt=start)

        def get_archived(self, days=14):
            start = datetime.datetime.now()-datetime.timedelta(days)
            return self.filter(date__lt=start)

    def __unicode__(self):
        return '%s: %d from %s to %s' % (self.get_criterion_display(), self.value, self.from_user, self.to_user)

    def get_actual(self):
        return self.objects.filter(date__min=util.create_date_range(14))

    def get_datetime_distance(self):
        last = self.date.replace(tzinfo=utc)
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        distance = dt.distance_of_time_in_words(last, 1, now)
        return distance

    @staticmethod
    def get_criterion_title(criterion_id):
        return Mark.CRITERIA[int(criterion_id)-1][1]

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    active_criteria = models.CommaSeparatedIntegerField(max_length=20)

    def __unicode__(self):
        return '%s\'s profile' % (self.user.username)


class MarkAdmin(admin.ModelAdmin):
    list_display = ('value', 'to_user', 'from_user', 'criterion')

