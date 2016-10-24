# import python native
import json

# import flask
from flask import Flask, jsonify, request
from flask_login import LoginManager

# import Mongo Exceptions
from mongoengine import *

# import local
from . import db_config
from . import db_models

login_manager = LoginManager()
schedule_app = Flask(__name__)
login_manager.init_app(schedule_app)

# configure the app
schedule_app.config["SECRET_KEY"] = db_config.SECRET_KEY


@login_manager.user_loader
def load_user(pid):
    try:
        return models.User.objects.get(pid=pid)
    except MultipleObjectsReturned as e:
        return None
    except DoesNotExist as e:
        return None

@schedule_app.route("/")
def index():
    return "It works"

@schedule_app.route("/db/test/create_user")
def db_test():
    try:
        pid = request.args.get('pid')
        u = models.User()
        u.init(pid=pid)
        u.save()
    except NotUniqueError:
        return "ERROR: Attempted to create user with non-unique pid."
    return u.to_json()

@schedule_app.route("/db/test/list_users")
def db_users():
    try:
        return models.User.objects.to_json()
    except DoesNotExist:
        return "ERROR: Database does not contain any users"
    except:
        return "ERROR: Something else went wrong."

@schedule_app.route("/db/test/delete_user")
def db_delete_user():
    pid = request.args.get('pid')
    try:
        while(True):
            if pid == 'all':
                u = models.User.objects
                if u.to_json() != []:
                    u = u.first()
            elif pid is None:
                return "Specify pid of user to delete"
            else:
                u = models.User.objects.get(pid=pid)
            u.delete()
    except:
        return "Done"
    return "Done"

# Import app views
from .api import user_views
