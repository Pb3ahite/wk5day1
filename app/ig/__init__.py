from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from ..models import db, User
from ..api import api


from flask import Blueprint

ig = Blueprint('ig', __name__, template_folder='ig_templates')

from . import routes