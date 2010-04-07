from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext

from four_schedules.scrapers.schedules import HouseFloorSchedule

def index(request):
    house_floor = HouseFloorSchedule().as_json()
    return render_to_response('index.html', {'house_floor': house_floor})
