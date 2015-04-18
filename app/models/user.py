__author__ = 'Peter Johnston'
# FitTrackr April 12, 2015

import hashlib
from uuid import uuid1
from bson.objectid import ObjectId

class User():
    """
    Represents a User object
    """
    def __init__(self, _id, password, email, login_hash, 
                 date_added, date_modified, workouts = []):
        """
        Construct a User object
        """
        if _id is None:
            new_id = ObjectId()
        else:
            new_id = _id
        if login_hash is None:
            self.hash = uuid1()
        else:
            self.hash = login_hash
        self._id = new_id
        self.password = password
        self.email = email
        self.date_added = date_added
        self.date_modified = date_modified
        self.authenticated = True
        self.active = True
        self.anonymous = False
        self.workouts = workouts

    def get_workouts(self):
        return self.workouts

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    @staticmethod
    def hide_user_password(password):
        """
        Hash the given string using md5
        """
        md5 = hashlib.md5(password)
        return md5.hexdigest()

    def get_id(self):
        return unicode(self._id)

    def get_hash(self):
        return unicode(self.hash)