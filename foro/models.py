from email.policy import default
from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    profile_photo = db.Column(db.String(120), nullable=True, default="default.webp")
    profile_banner = db.Column(db.String(120), nullable=True, default="default.jpg")
    profile_background = db.Column(db.String(120), nullable=True)
    last_connection = db.Column(db.String(120), nullable = False)
    is_active = db.Column(db.DateTime(timezone=True), default= datetime.utcnow())
    comments = db.relationship('Comment', cascade="all, delete", backref="user")
    likes = db.relationship('Comment_Like', cascade="all, delete", backref="user")
    posts = db.relationship('Post', cascade="all, delete", backref="user")
    subs = db.relationship('Subs', cascade="all, delete", backref="user")

class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=True)
    profile_id = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'))
    likes = db.relationship('Comment_Like',cascade="all, delete", backref="comment")

class Comment_Like(db.Model):
    __tablename__ = 'CommentLike'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('Comment.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

class Post_Category(db.Model):
    __tablename__ = 'PostCategory'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120), nullable=True)
    name = db.Column(db.String(100), nullable=True, unique=True)
    posts = db.relationship('Post', cascade="all, delete", backref="post_category")

class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.String(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('PostCategory.id'))
    likes = db.relationship('Comment_Like', cascade="all, delete" ,backref="post")
    comments = db.relationship('Comment', cascade="all, delete" ,backref="post")

class Subs(db.Model):
    __tablename__ = 'Subs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    profile_id = db.Column(db.Integer)

