__author__ = 'Peter Johnston'
# FitTrackr April 12, 2015

from pymongo import MongoClient

# Connect to our MongoDB pickle payments database
client = MongoClient()
db = client.fittrackr