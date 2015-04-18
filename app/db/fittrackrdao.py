__author__ = 'Peter Johnston'
# FitTrackr April 12, 2015

from bson.objectid import ObjectId
from datetime import datetime

class FitTrackrDAO(object):
    """
    FitTrackrDao is the base Dao object for FitTrackr. All Daos extend this class
    to perform basic CRUD operations
    """
    def __init__(self, database, collection):
        """
        Connect to the proper database and the proper collection
        """
        self.db = database
        self.collection = collection

    def insert_obj(self, obj):
        """
        Insert the given object into the collection
        All entities inserted must have a date_added field, which is set to the current time when inserted
        Return the id
        """
        if obj.date_added is not None:
            print obj.date_added
        return self.collection.insert(dict(obj.__dict__.items() +
                { 'date_added' : datetime.now(), 'date_modified' : datetime.now() }.items()))

    def update_obj(self, obj):
        """
        Update the object passed in. Obj represents the updated version of the original item. Must have
        a real id to function.
        """
        obj.__dict__.update(date_modified = datetime.today())
        return self.collection.save(obj.__dict__)

    def find_all(self):
        """
        Find all objects stored in the collection
        """
        obj_list = []
        for each_obj in self.collection.find():
            if each_obj is not None:
                obj_list.append(each_obj)
        return obj_list

    def find_by_id(self, _id):
        """
        Find the object with the given id
        """
        obj = self.collection.find_one({"_id": ObjectId(_id)})
        return obj

    def remove_all(self):
        """
        Remove all objects from the collection
        """
        self.collection.remove()