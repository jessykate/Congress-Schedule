#!/usr/bin/python

try:
    import json
except:
    import simplejson as json

from BeautifulSoup import BeautifulSoup
import urllib2, sys, re


class SenateFloorSchedule(object):
    def __init__(self):
        self.get_html()
        
    def get_html(self):
        ''' get the html markup corresponding to the senate schedule'''
        url = "http://www.senate.gov/pagelayout/legislative/d_three_sections_with_teasers/calendars.htm"
        fp = urllib2.urlopen(url)
        # the converEntities argument will turn html entities like
        # #&xxx; back into synbols.
        self.soup = BeautifulSoup(fp.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)                
    
    def parse(self):
        # get the first contentsubtitle, which is the current or
        # upcoming schedule.
        self.sched = {
            'date' :  self.soup.find(attrs={'class':'contentsubtitle'}).findNext().text,
            'agenda' : self.soup.find(attrs={'class':'contentsubtitle'}).findNext().findNext().text,
            }
        return self.sched

    def as_json(self):
        return json.dumps(self.parse())
 

class HouseFloorSchedule(object):
    def __init__(self, date='today'):
        ''' initializes a house floor schedule object with various
        information needed to parse the html, and then retrieves the
        html.'''

        if date != 'today':
            print 'not implemented.'
            sys.exit()

        # prefix notes appear before te actual schedule items
        self.announcements_prefix = "members are advised"

        # schedule headings are not structurally unique in the html
        # but seem to adhere to a consistent set of text
        # strings. note: 'suspension' sometimes appears in the
        # singular so leave it as such here to catch both cases.
        self.schedule_heading_prefixes = ["one minutes", 
                                          "suspension", 
                                          "postponed suspension", 
                                          "dispose of", 
                                          "complete consideration", 
                                          "begin consideration", 
                                          "conference report", 
                                          "continue consideration", 
                                          "motion to",
                                          "possible consideration",
                                          "h.r.", 
                                          "h.con.res.", 
                                          "h.res", 
                                          "h.j.res",     
                                          ]
        # when building the agenda, we track if we're in suspensions
        # or postponements. if not, the default is 'other'. 
        self.current_agenda_subsection = 'other'
    
        # these appear to be at the bottom of each day's schedule. 
        self.schedule_footnotes = ["conference reports may be brought up at any time", 
                                   "motions to go to conference should they become available", 
                                   "possible motions to instruct conferees"]

        self.get_html(date)

    def parse(self):
        ''' builds a dictionary with the schedule information from html'''
        self.schedule = {
            'date': None,
            'start_meet': None,
            'start_vote': None,
            'end_vote': None,
            'agenda': None        
            }
        self.get_date()
        self.get_start_meet()
        self.get_start_vote()
        self.get_end_vote()
        self.get_agenda()

        # pull out links to bills on thomas
        # (find links for opencongress?)
        # 


    def as_json(self):
        return json.dumps(self.parse())

    def get_html(self, date):
        ''' get the html markup corresponding to the schedule on the date specified'''
        fp = urllib2.urlopen(self.get_schedule_url(date))
        # the converEntities argument will turn html entities like
        # #&xxx; back into synbols.
        self.soup = BeautifulSoup(fp.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)

    def get_schedule_url(self, date):
        # call this url with the start parameter equal to the number of
        # records back to go. ie, the most current agenda will show up
        # when called with start=1. so with start=n, the top record
        # displayed on the page will be that from n-1 days ago.
        # 
        # http://majorityleader.gov/links_and_resources/whip_resources/dailyleader.cfm?start=2

        url = "http://majorityleader.gov/links_and_resources/whip_resources/currentdailyleader.cfm"
        #url = "http://majorityleader.gov/links_and_resources/whip_resources/dailyleader.cfm?pressReleaseID=4022"
        return url
        
    def get_date(self):
        date_header = (self.soup.table.findNext('tbody').findNext('tr').
                       findNext('td').findNext('td').findNext('strong').text)

        # the date format seems to be fine for javascript parsers, so
        # leave it as it. eg. SATURDAY, MARCH 20, 2010
        try:
            self.schedule['date'] = date_header.split('FLOOR SCHEDULE FOR ')[1]    
        except:
            self.schedule['date'] = None
            
    def get_start_meet(self):
        self.schedule['start_meet'] = (self.soup.table.findNext('tbody').findNext('table').
                                       findNext('tbody').findNext('tr').
                                       findNext('strong').findNext('span').text.strip())

    def get_start_vote(self):
        self.schedule['start_vote'] = (self.soup.table.findNext('tbody').findNext('table').
                                       findNext('tbody').findNext('tr').findNext('strong').
                                       findNext('strong').findNext('span').text.strip())

    def get_end_vote(self):
        self.schedule['end_vote'] = (self.soup.table.findNext('tbody').findNext('tbody').
                                     findNext('tr').findNext('td').findNext('strong').
                                     findNext('strong').findNext('strong').text.strip())

    def check_for_announcements(self, text):
        if self.announcements_prefix in text:
            self.schedule['agenda']['announcements'].append(text)
            return True
        return False

    def check_for_footnotes(self, text):
        for footnote in self.schedule_footnotes:
            if footnote in text:
                self.schedule['agenda']['footnotes'].append(text)                    
                return True
        return False

    def add_to_agenda_item(self, item, text):
        # if it has a parent tag that is a list item then it's not a
        # section heading. (should add search for parent style that's
        # an "mso-list" such as on nov.6, 2009. 
        if not item.findParent('li'):
            # check to see if this matches any known headings. if so,
            # start a new (empty) schedule item.
            for heading in self.schedule_heading_prefixes:
                if heading in text:
                    print 'heading found: %s' % text
                    #self.schedule['agenda']['items'].append('')
                    # check if we're in a subsection or not. 
                    if 'postponed suspension' in text:
                        self.current_agenda_subsection = 'postponements'
                        #self.schedule['agenda']['postponements'].append('')
                    elif 'suspension' in text: # this has to go second
                        self.current_agenda_subsection = 'suspensions'
                        #self.schedule['agenda']['suspensions'].append('')
                    else: 
                        self.current_agenda_subsection = 'other'
                        #self.schedule['agenda']['other'].append('')

        # whatever the current schedule item, append the text to
        # it. if it was determined above to be a heading, then this
        # will be the first line for this item. else, it will just be
        # appended to the current item.
        section = self.current_agenda_subsection
        #self.schedule['agenda'][section][-1] += ' '+text
        self.schedule['agenda'][section].append(text)

    def get_agenda(self):
        self.schedule['agenda'] = {'announcements': [], 'suspensions': [], 'postponements': [], 'other': [], 'footnotes': []}
        agenda = (self.soup.table.findNext('tbody').findNext('tr').
                  findNext('td').findNext('div', unselectable="off"))

        for line in agenda.findAll(text=True):   
            # normalize case and strip whitespace
            text = line.lower().strip()            
            if not text: continue
            if not self.check_for_announcements(text):
                if not self.check_for_footnotes(text):
                    self.add_to_agenda_item(line, text)


def senate_floor_current():
    pass

def house_committee_current():
    pass

def senate_committee_current():
    pass

if __name__ == '__main__':
    senate_sched = SenateFloorSchedule()
    sched = senate_sched.as_json()
    print 'Senate Floor Current Schedule\n'
    print sched
    print ""

    print 'House Floor Current Schedule\n'
    house_sched = HouseFloorSchedule("today")
    sched = house_sched.as_json()
    for k,v in json.loads(sched).iteritems():
        print "========== %s ============" % k
        if k == 'agenda':
            if v['announcements']:
                print "========== Announcements ============"
                for item in v['announcements']:
                    print item

            if v['other']:
                print "========== Other ============"
                for item in v['other']:
                    print '\t'+item

            if v['suspensions']:
                print "========== Suspensions ============"
                for item in v['suspensions']:
                    print '\t'+item

            if v['postponements']:
                print "========== Postponents ============"
                for item in v['postponements']:
                    print '\t'+item

            if v['footnotes']:
                print "========== Footnote Items ============"
                for item in v['footnotes']:
                    print item

        else:
            print v

