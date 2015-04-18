__author__ = 'Peter Johnston'
# FitTrackr April 12, 2015

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager

from app.secretkey import SECRET_KEY

app = Flask(__name__)

# Bootstrap configuration
bootstrap = Bootstrap(app)

#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"
# Initialize app secret key
app.secret_key = SECRET_KEY

from views import index, dashboard