import pymongo
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from four_schedules.scrapers.schedules import (HouseFloorSchedule, 
                                               SenateFloorSchedule,
                                               SenateCommitteeSchedule,
                                               HouseCommitteeSchedule)
from pymongo import Connection


def committee_schedule(chamber):
    connection = Connection()
    db = connection.schedules
    collection = db.committee_hearing
    events = []
    for event in collection.find({'chamber':chamber}):
        events.append(event)
    return events                                  

def index(request):
    house_floor_url = "http://majorityleader.gov/links_and_resources/whip_resources/currentdailyleader.cfm"
    senate_floor_url = "http://www.senate.gov/pagelayout/legislative/d_three_sections_with_teasers/calendars.htm"
    senate_floor = SenateFloorSchedule().parse()
    house_floor = HouseFloorSchedule().parse()
    senate_cmte = committee_schedule('Senate')
    house_cmte = committee_schedule('House')
    return render_to_response('front_end/index.html', 
                              {'senate_floor': senate_floor, 
                               'house_floor': house_floor,
                               'senate_cmte': senate_cmte,
                               'house_cmte': house_cmte,
                               'house_floor_source': house_floor_url,
                               'senate_floor_source': senate_floor_url,
                               }
                              )
