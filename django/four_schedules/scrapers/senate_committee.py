# senate_committee.py
# Updated 4/24/2010 -- Josh Ruihley
# Import Senate Committee Hearing Schedule from Real Time Congress API 

import pymongo, simplejson, urllib
from pymongo import Connection

connection = Connection()
db = connection.schedules
collection = db.senate_committee

url = 'http://realtimecongress.org/hearings_upcoming.json?chamber=Senate'
hearings = simplejson.load(urllib.urlopen(url))
for hearing in hearings:
    if not collection.find_one(hearing):
        collection.insert(hearing)