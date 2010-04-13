from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from four_schedules.scrapers.schedules import HouseFloorSchedule, SenateFloorSchedule

def index(request):
    senate_floor = SenateFloorSchedule().as_json()
    return render_to_response('front_end/index.html', {'senate_floor': senate_floor})