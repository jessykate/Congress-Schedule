from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext

<<<<<<< HEAD:django/four_schedules/front_end/views.py
from four_schedules.parsers.schedules import HouseFloorSchedule, SenateFloorSchedule
=======
from four_schedules.scrapers.schedules import HouseFloorSchedule
>>>>>>> b61ab5b6b4b7332b6f862c5d34be92e496bf58ff:django/four_schedules/front_end/views.py

def index(request):
    senate_floor = SenateFloorSchedule().as_json()
    return render_to_response('index.html', {'senate_floor': senate_floor})