__author__ = 'Peter Johnston'
# FitTrackr April 18, 2015

from bson.objectid import ObjectId

class Exercise():
    """
    Represents an Exercise object
    """
    TYPE_RESISTANCE = 'RESISTANCE'
    TYPE_CARDIO = 'CARDIO'
    types = [TYPE_RESISTANCE, TYPE_CARDIO]

    def __init__(self, _id, name, _type, date_added, date_modified):
        if _id is None:
            new_id = ObjectId()
        else:
            new_id = _id
        self.name = name
        if _type in self.types:
            self._type = _type
        else:
            raise Exception('Exercise type is invalid')
        self.date_added = date_added
        self.date_modified = date_modified