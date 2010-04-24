# senate_committee.py
# Updated 4/24/2010 -- Josh Ruihley
# Import Senate Committee Hearing Schedule from Real Time Congress API 

import pymongo, simplejson, urllib
from pymongo import Connection

connection = Connection()
db = connection.schedules
collection = db.committee_hearing
chambers = ['House', 'Senate']

for chamber in chambers:
    url = 'http://realtimecongress.org/hearings_upcoming.json?chamber=%s' % chamber
    hearings = simplejson.load(urllib.urlopen(url))
    for hearing in hearings:
        hearing['chamber'] = chamber
        if not collection.find_one(hearing):
            collection.insert(hearing)