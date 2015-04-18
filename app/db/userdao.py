__author__ = 'Peter Johnston'
# FitTrackr April 12, 2015

from app.db.fittrackrdao import FitTrackrDAO

class UserDAO(FitTrackrDAO):
    """
    Handles interactions with the database involving a User object
    """
    def __init__(self, database):
        """
        Connect to the proper database and the proper user collection
        """
        self.collection = database.user
        FitTrackrDAO.__init__(self, database, self.collection)

    def find_user_by_email(self, email_address):
        """
        Find a user in the collection with the given email address
        """
        user = self.collection.find_one({'email': email_address})
        if user is not None:
            return user

    def find_user_by_hash(self, hash_id):
        """
        Find a user in the collection with the given hash
        """
        try:
            user = self.collection.find_one({'hash': hash_id})
            if user is not None:
                return user
        except KeyError:
            # TODO Do something with the error
            print 'Key Error bro!'