#!/usr/bin/python

try:
    import json
except:
    import simplejson as json

from BeautifulSoup import BeautifulSoup
import urllib2


def house_floor_current():
    fp = urllib2.urlopen("http://majorityleader.gov/links_and_resources/whip_resources/currentdailyleader.cfm")
    soup = BeautifulSoup(fp.read())

    # a note about navigating the parse tree with beautiful soup: dont
    # want to be too dependent on the existing page structure by
    # specifying every element of every step. on the other hand, want
    # to be specific enough that newly introduced elements don't break
    # our parsing scheme.

    js = {
        'date': None,
        'start_meet': None,
        'start_vote': None,
        'end_vote': None,
        'agenda': None        
        }

    date_header = soup.table.findNext('tbody').findNext('tr').findNext('td').findNext('td').findNext('strong').text
    # the date format seems to be fine for javascript parsers, so leave it as it. 
    # eg. SATURDAY, MARCH 20, 2010
    js['date'] = date_header.split('FLOOR SCHEDULE FOR ')[1]    

    # get start and end times for this session 
    js['start_meet'] = soup.table.findNext('tbody').findNext('table').findNext('tbody').findNext('tr').findNext('strong').findNext('span').text
    js['start_vote'] = soup.table.findNext('tbody').findNext('table').findNext('tbody').findNext('tr').findNext('strong').findNext('strong').findNext('span').text
    js['end_vote'] = soup.table.findNext('tbody').findNext('table').findNext('tbody').findNext('tr').findNext('strong').findNext('strong').findNext('strong').findNext('span').text

    # get the agenda as one blob of text. we do this because
    # apparently we don't believe in headers anymore, so there's no
    # good way to consistently differentiate between categories of
    # agenda items and the agenda items themselves.
    agenda = soup.table.findNext('tbody').findNext('tr').findNext('td').findNext('div', unselectable="off")
    # take out all the retarded markup
    for elem in agenda.findAll(True):
        elem.attrs = []
    # fix the escaped chars, then get rid of extra whitespace and the
    # now-useless <span> elements. 
    for elem in agenda.findAll(True):
        if elem.name == 'span':
            # get the children and replace the span element with its own subtree
        
       

    return json.dumps(js)

def house_floor(date='today'):
    if date == 'today':
        return house_floor_current()
    # call this url with the start parameter equal to the number of
    # records back to go. ie, the most current agenda will show up
    # when called with start=1. so with start=n, the top record
    # displayed on the page will be that from n-1 days ago.
    # 
    # http://majorityleader.gov/links_and_resources/whip_resources/dailyleader.cfm?start=2
        
    # grab the top url and follow it. 


def senate_floor_current():
    pass

def house_committee_current():
    pass

def senate_committee_current():
    pass

if __name__ == '__main__':
    print 'house floor current schedule\n'
    print house_floor_current()
