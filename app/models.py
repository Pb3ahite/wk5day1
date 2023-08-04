
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    posts = db.relationship("Post", backref='author')
    Liked_posts2 = db.relationship("Post", secondary='like2')
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

    
    followers = db.relationship("User",  
                                secondary=followers,
                                lazy='dynamic',
                                backref=db.backref('followed', lazy='dynamic'),
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id)
                                )

    def __init__(self, username, email, password, first_name, last_name):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
    def get_liked_pokemon(self):
        ps = Liked_Pokemon.query.filter_by(user_id=self.id).all()
        return ps


    

like2 = db.Table('like2',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable=False)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likers2 = db.relationship('User', secondary='like2')

    def __init__(self, title, caption, image_url, user_id):
        self.title = title
        self.caption = caption
        self.img_url = image_url
        self.user_id = user_id

    def like_count(self):
        return len(self.likers2)
    
class Liked_Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id, name):
        self.name=name
        self.user_id=user_id  






