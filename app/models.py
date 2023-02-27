import email
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import url_for

#  from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class APIMixin(object):
    @staticmethod
    def to_collection_dict(query):
        resources = query.paginate()
        print(resources)
        data = {
            'items': [item.to_dict() for item in resources.items]
            }
        
        return data

class User(APIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(64), index = True, unique = True)
    mobile = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="parrent", lazy = "dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def posts(self):
    #     my_posts = 

 

    def to_dict(self, include_email = False):
        data =  {
            "id" : self.id,
            "name" : self.username,

            }
        

        return data





class Post(APIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    title = db.Column(db.String(64), index = True)
    category_id = db.Column(db.Integer,ForeignKey("category.id"), default = 1)
    body = db.Column(db.String(256))
    price = db.Column(db.Integer, default = 0)
    PSC = db. Column(db.Integer)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)


    def to_dict(self):
        posts = {
            "post id" : self.id,
            "user id" : self.user_id,
            "user" : self.parrent.username,
            "title" : self.title,
            "body" : self.body
        }

        return posts

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    image = db.Column(db.String(64), default = "")
    postCat = db.relationship("Post", backref="postCat", lazy = "dynamic")