from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment



app = Flask(__name__)
app.config.from_object(Config)
from .api import api
from .ig import ig

app.register_blueprint(api)
app.register_blueprint(ig)
from .models import db, User
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
moment = Moment(app)

@login_manager.user_loader
def load_user(user_id):

    #return User.query.filter_by(id=user_id).first()
    return User.query.get(user_id)


login_manager.login_view='login_page'

from . import routes, models