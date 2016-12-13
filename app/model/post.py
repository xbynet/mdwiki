from datetime import datetime

from app.extensions import db
from app import util

import uuid

post_tag = db.Table('post_tag', db.Column('tag_id', db.String(100), db.ForeignKey('tag.id')),
                    db.Column('post_id', db.String(100), db.ForeignKey('post.location')))


class Post(db.Model):
    # id=db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String(100), primary_key=True)
    tags = db.relationship('Tag', secondary=post_tag,backref=db.backref('pages',lazy='dynamic'))# lazy='dynamic' #lazy='subquery'
    userId=db.Column(db.String(100))
    createAt=db.Column(db.DateTime(),default=datetime.now())

class Tag(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.id = str(uuid.uuid1())
        self.name = name

    def __repr__(self, *args, **kwargs):
        return '<Tag %s>' % self.name

