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
    return render_template('dashboard.html', workout_list=current_user.workouts[0:3])

@app.route("/dashboard/workouts")
@login_required
def user_workouts():
    return render_template('workouts.html', workout_list=current_user.workouts)

@app.route("/trackWorkout")
@login_required
def track_workout():
    return render_template('trackworkout.html', exercises=exercise_dao.find_all(), exercise_types=Exercise.types)

@app.route("/saveWorkout", methods=['POST'])
@login_required
def save_workout():
    workout_date = str(request.form['dateOfWorkout'])
    this_workout = { 'workout_id' : uuid1(), 'date_performed' : datetime.strptime(workout_date, "%m/%d/%Y") }
    # TODO may be some wonkiness if the user presses the back button
    for each in request.form:
        if each != 'dateOfWorkout':
            current = request.form[each].split('~')
            exercise_name = current[0]
            weights = current[1]
            sets = current[2]
            reps = current[3]
            this_workout = dict(this_workout.items() + { 'exercise' : exercise_name, 'weights' : weights, 
                'sets' : sets, 'reps' : reps }.items())
    current_user.workouts.append(this_workout)
    current_user.workouts = multikeysort(current_user.workouts, ['-date_performed'])
    user_dao.update_obj(current_user)

    return render_template('dashboard.html')

@app.route("/addExerciseToList", methods=['POST'])
def add_exercise_to_list():
    data = json.loads(request.data)
    data['isValid'] = True
    return json.dumps(data)

@app.route("/addExerciseToDatabase", methods=['POST'])
def add_exercise_to_database():
    exercise_name = request.form['newExerciseName']
    exercise_type = request.form['newExerciseType']
    exercise_dao.insert_obj(Exercise(None, exercise_name, exercise_type, None, None))
    return redirect(redirect_url())

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