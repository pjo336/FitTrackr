__author__ = 'Peter Johnston'
# FitTrackr April 18, 2015

from flask import render_template
from flask import request
from flask import redirect
from app.flask_login import login_required
from app.flask_login import current_user
from app import app
from app.db import db
from app.db.exercisedao import ExerciseDAO
from app.db.userdao import UserDAO
from app.models.user import User
from app.models.exercise import Exercise
from datetime import datetime
from uuid import uuid1
import json

user_dao = UserDAO(db)
exercise_dao = ExerciseDAO(db)

@app.route("/dashboard")
@login_required
def user_dashboard():
    """
    Sort the users workouts by date performed and return the 3
    most recent to the dashboard template.
    """
    workouts = multikeysort(current_user.workouts, ['-date_performed'])
    return render_template('dashboard.html', workout_list=workouts[0:3])

@app.route("/dashboard/workouts")
@login_required
def user_workouts():
    """
    Return all the users workouts.
    """
    return render_template('workouts.html', workout_list=current_user.workouts)

@app.route("/trackWorkout")
@login_required
def track_workout():
    """
    Return all the exercises and exercise types.
    """
    return render_template('trackworkout.html', exercises=exercise_dao.find_all(), exercise_types=Exercise.types)

@app.route("/saveWorkout", methods=['POST'])
@login_required
def save_workout():
    """
    Create a workout with the given data.
    First create an id, and set the date performed into a new dict.
    Next, iterate over each exercise object in the request form. 
    Split the string for each exercise which is in the format:
        exercise_name~weight_performed~sets_performed~reps_performed
    Append these objects to the workout dict.
    Finally, add this workout to the current_users workout list and
    update the user object.
    """
    workout_date = str(request.form['dateOfWorkout'])
    this_workout = { 'workout_id' : uuid1(), 'date_performed' : datetime.strptime(workout_date, "%m/%d/%Y") }
    # TODO may be some wonkiness if the user presses the back button
    excercise_list = []
    for each in request.form:
        if each != 'dateOfWorkout':
            current = request.form[each].split('~')
            exercise_name = current[0]
            exercise = exercise_dao.find_exercise_by_name(exercise_name)
            weights = current[1]
            sets = current[2]
            reps = current[3]
            excercise_list.append( { 'exercise': exercise, 'weights' : weights, 
                'sets' : sets, 'reps' : reps } )
    # Add the list of exercises performed to the days workout
    this_workout['exercises'] = excercise_list
    # Add to the users workout list
    current_user.workouts.append(this_workout)
    #current_user.workouts = multikeysort(current_user.workouts, ['-date_performed'])
    user_dao.update_obj(current_user)

    return render_template('dashboard.html')

@app.route("/addExerciseToList", methods=['POST'])
def add_exercise_to_list():
    """
    Adds the exercise in the request to the html on the page
    TODO this is an unnecessary method.
    """
    data = json.loads(request.data)
    data['isValid'] = True
    return json.dumps(data)

@app.route("/addExerciseToDatabase", methods=['POST'])
def add_exercise_to_database():
    """
    Add the given exercise in the request form to the database
    """
    exercise_name = request.form['newExerciseName']
    exercise_type = request.form['newExerciseType']
    exercise_dao.insert_obj(Exercise(None, exercise_name, exercise_type, None, None))
    return redirect(redirect_url())

@app.route("/deleteWorkout", methods=['POST'])
def delete_workout():
    """
    Delete the workout with the id sent inside the request.data.
    Iterates over each workout in the current user, finds the workout
    with the id, then removes it from the workout list and updates the user
    """
    data = json.loads(request.data)
    for index, each in enumerate(current_user.workouts):
        if str(each['workout_id']) == str(data):
            print 'worked'
            del current_user.workouts[index]
            user_dao.update_obj(current_user)
            return json.dumps( {'isValid': True} )
    # Id wasn't found, return not valid
    return json.dumps( {'isValid': False} )

# Found on stackoverflow
def multikeysort(items, columns):
    from operator import itemgetter
    comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else
                  (itemgetter(col.strip()), 1)) for col in columns]
    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0
    return sorted(items, cmp=comparer)

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)