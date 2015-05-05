__author__ = 'Peter Johnston'
# FitTrackr April 14, 2015

from app.db.fittrackrdao import FitTrackrDAO

class ExerciseDAO(FitTrackrDAO):
    """
    Handles interactions with the database involving a Excercise object
    """
    def __init__(self, database):
        """
        Connect to the proper database and the proper user collection
        """
        self.collection = database.exercise
        FitTrackrDAO.__init__(self, database, self.collection)

    def find_exercise_by_name(self, name):
        """
        Find the exercise in the collection with the given name
        """
        exercise = self.collection.find_one({'name': name})
        if exercise is not None:
            return exercise