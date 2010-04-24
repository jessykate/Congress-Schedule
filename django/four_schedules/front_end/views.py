import pymongo
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from four_schedules.scrapers.schedules import (HouseFloorSchedule, 
                                               SenateFloorSchedule,
                                               committee_schedule,
                                               SenateCommitteeSchedule,
                                               HouseCommitteeSchedule)

def index(request):
    #Source Info
    house_floor_url = "http://majorityleader.gov/links_and_resources/whip_resources/currentdailyleader.cfm"
    senate_floor_url = "http://www.senate.gov/pagelayout/legislative/d_three_sections_with_teasers/calendars.htm"
    senate_cmte_url = "http://www.senate.gov/pagelayout/committees/one_item_and_teasers/committee_hearings.htm"
    house_cmte_url = "http://www.house.gov/daily/comlist.html"
    
    #Event Schedules
    senate_floor_events = SenateFloorSchedule().parse()
    house_floor_events = HouseFloorSchedule().parse()
    senate_cmte_events = committee_schedule('Senate')
    house_cmte_events = committee_schedule('House')
    
    house_floor = {'url':house_floor_url, 'events':house_floor_events}
    senate_floor = {'url':senate_floor_url, 'events':senate_floor_events}
    senate_cmte = {'url':senate_cmte_url, 'events':senate_cmte_events}
    house_cmte = {'url':house_cmte_url, 'events':house_cmte_events}

    return render_to_response('front_end/index.html', 
                              {'senate_floor': senate_floor, 
                               'house_floor': house_floor,
                               'senate_cmte': senate_cmte,
                               'house_cmte': house_cmte,
                               }
                              )
