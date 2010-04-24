# import_floor_schedules.py
# Updated 4/24/2010 -- Josh Ruihley
# Save House and Senate Floor Schedules to db

import pymongo, simplejson, urllib
from schedules import HouseFloorSchedule, SenateFloorSchedule
from pymongo import Connection

connection = Connection()
db = connection.schedules

house_collection = db.house_floor
senate_collection = db.senate_floor

house_floor = HouseFloorSchedule().parse()
if not house_collection.find_one(house_floor):
    house_collection.insert(house_floor)
    
senate_floor = SenateFloorSchedule().parse()
if not senate_collection.find_one(senate_floor):
    senate_collection.insert(senate_floor)