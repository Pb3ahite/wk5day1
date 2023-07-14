from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
#

    #@login_manager.user_loader
    #def load_user(user id):
        #return User.query.filter_by(id=user_id)
        #return User.query.get(user_id)


from . import routes