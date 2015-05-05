__author__ = 'Peter Johnston'
# FitTrackr April 12, 2015

from flask import render_template
from flask import request
from app.flask_login import login_user
from app.flask_login import logout_user
from flask import redirect
from flask import session
from app import app
from app import login_manager
from app.db import db
from app.db.userdao import UserDAO
from app.models.user import User


# User DAO
user_dao = UserDAO(db)

@app.route("/index", methods=['GET'])
@app.route("/index.html", methods=['GET'])
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/signup", methods=['GET'])
def signup_form():
	return render_template('signup.html')

@app.route("/signup", methods=['POST'])
def signup_form_submit():
    # Retrieve the information from the form
    email = request.form.get('email')
    password = User.hide_user_password(request.form.get('password'))
    new_user = User(None, password, email, None, None, None)
    # Insert the record using our UserDao
    user_dao.insert_obj(new_user)
    return render_template('index.html', users = user_dao.find_all())

@login_manager.user_loader
def load_user(userid):
    user = user_dao.find_by_id(userid)
    return User(user['_id'], user['password'], user['email'], user['hash'],
                user['date_added'], user['date_modified'], user['workouts'])

@app.route("/login", methods=['GET'])
def serve_login_page():
    """
    Serve the initial login page
    """
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def post_login_page():
    """
    Submit the login form
    """
    email = request.form['userEmail']
    password = User.hide_user_password(request.form['userPassword'])
    #rememberMe = request.form['rememberMe']
    # Note this is just a dict, not an actual user
    user = user_dao.find_user_by_email(email)
    # Login was not successful, tell the user
    try:
        if user is None or user['password'] != password:
            return render_template('login.html',
                                   message='The email or password you entered is incorrect')
    except AttributeError:
        return render_template('login.html',
                               message='The email or password you entered is incorrect')

    hash_formula = user['hash']
    # Login was successful so officially log the user is and add their hash to the session
    # Remember this is just a dict and not an actual User object, we need to login an
    # actual User
    user_obj = User(user['_id'], user['password'], user['email'],
                    user['hash'], user['date_added'], user['date_modified'], user['workouts'])
    login_user(user_obj)
    session['username'] = hash_formula
    return redirect('/')

@app.route("/logout")
def logout():
    """
    Log the current user out then pop off the session cookie
    """
    try:
        if session['username'] is not None:
            logout_user()
            session.pop('username', None)
        return redirect('/')
    except KeyError:
        print 'KEYYyyyyyyyyyyyy errrorrrr'
        return redirect('/')

@app.route("/gif")
def gif():
    return render_template('gif.html')
