from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from main.models import Mark
from django.db.models import Avg
from django.utils import simplejson
from datetime import datetime, timedelta
from django.utils import timezone
from main import util
from django.contrib import auth
# Create your views here.

def start(request):
    if request.user.is_authenticated():
        return redirect('/%s' % (request.user.username))
    else:
        return redirect('/login/')



def profile(request, username):
    user = User.objects.get(username=username)
    last_date = datetime.now() - timedelta(days=14)

    fullname = user.get_full_name()
    #received_marks = user.received_marks.filter(date__range=util.create_date_range(14))
    received_marks = user.received_marks.all().get_actual()
    count = len(received_marks)
    overall_rating = 0
    if count > 0:
        overall_rating = "%.2f" % received_marks.aggregate(Avg('value'))["value__avg"]
        received_marks_grouped = util.group_marks(received_marks)


    criteria = user.profile.active_criteria.split(',')
    criterial_rating = []
    for criterion in criteria:
        c_marks = received_marks.filter(criterion=criterion)
        c_count = len(c_marks)
        c_overall = 0
        if len(c_marks) > 0:
            c_overall = c_marks.aggregate(Avg('value'))["value__avg"]

        #percent = c_overall*10
        cat_title = Mark.get_criterion_title(criterion)
        new_allowed = False
        if request.user.is_authenticated():
            new_allowed = util.is_new_mark_allowed(request.user, user, criterion)

        criterial_rating.append({
            'id': int(criterion),
            'overall': c_overall,
            'cat_title': cat_title,
            'count': c_count,
            'new_allowed': new_allowed
        })
    #link to profile in comments!!
    criterial_rating_json = simplejson.dumps(criterial_rating)
    hide_form = request.user.is_authenticated()
    return render_to_response("profile.html", locals())

def rate(requset):
    if not requset.is_ajax():
        return HttpResponse(status=500)

    criterion_id = requset.GET['criterion_id']
    value = requset.GET['value']
    from_user = requset.user
    to_user = User.objects.get(id=requset.GET['to'])
    #comment = User.objects.GET['comment']

    if util.is_new_mark_allowed(from_user, to_user, criterion_id):
        new_mark = Mark(from_user=from_user, to_user=to_user, criterion=criterion_id, value=value, comment="")
        new_mark.save()
        return HttpResponse()
    else:
        return HttpResponse(status=500)

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:

        auth.login(request, user)

        return redirect("/account/loggedin/")
    else:

        return redirect("/account/invalid/")
