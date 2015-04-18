__author__ = 'Peter Johnston'
# FitTrackr April 18, 2015

from flask import render_template
from flask import request
from app.flask_login import login_required
from app.flask_login import current_user
from app import app
from app.db import db
from app.db.exercisedao import ExerciseDAO
from app.db.userdao import UserDAO
from app.models.user import User
from datetime import datetime
import json

user_dao = UserDAO(db)
exercise_dao = ExerciseDAO(db)


@app.route("/dashboard")
@login_required
def user_dashboard():
    print current_user._id
    return render_template('dashboard.html', workout_list=current_user.workouts)

@app.route("/trackWorkout")
@login_required
def track_workout():
    return render_template('trackworkout.html', exercises=exercise_dao.find_all())

@app.route("/saveWorkout", methods=['POST'])
@login_required
def save_workout():
    from uuid import uuid1
    this_workout = { 'workout_id' : uuid1(), 'date_performed' : datetime.now() }
    # TODO may be some wonkiness if the user presses the back button
    for each in request.form:
        current = request.form[each].split('~')
        exercise_name = current[0]
        weights = current[1]
        sets = current[2]
        reps = current[3]
        this_workout = dict(this_workout.items() + { 'exercise' : exercise_name, 'weights' : weights, 
            'sets' : sets, 'reps' : reps }.items())

    current_user.workouts.append(this_workout)
    user_dao.update_obj(current_user)

    return render_template('dashboard.html')

@app.route("/addExerciseToList", methods=['POST'])
def add_exercise_to_list():
    data = json.loads(request.data)
    data['isValid'] = True
    return json.dumps(data)
