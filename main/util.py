from main.models import Mark
import datetime
from django.utils import timezone
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.template import Library
from pytils import dt
import time

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return simplejson.dumps(object)

def group_marks(marks):
    common_list = []
    current_list = [marks[0]]
    for i in range(1, marks.count()):
        if not (marks[i].from_user == marks[i-1].from_user and (marks[i].date - marks[i-1].date).seconds < 300):
            common_list.append(current_list)
            current_list = []
        current_list.append(marks[i])
    common_list.append(current_list)
    return common_list

def is_new_mark_allowed(from_user, to_user, criterion_id):
    if from_user == to_user:
        return False
    try:
        last_date = Mark.objects.filter(from_user=from_user, to_user=to_user, criterion=criterion_id).order_by('-date')[0].date
    except:
        last_date = timezone.make_aware(datetime.datetime.min, timezone.get_default_timezone())

    now_date = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())

    diff = now_date - last_date

    if diff.days > 14:
        return True
    else:
        return False
