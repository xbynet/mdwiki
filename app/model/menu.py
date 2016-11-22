from app.extensions import db
import uuid

class Menu(db.Model):
    """ 菜单实体 """
    id=db.Column(db.String(100),primary_key=True)
    name=db.Column(db.String(25),unique=True)
    link=db.Column(db.String(50))
    icon=db.Column(db.String(10))
    active=db.Column(db.String(10))
    type=db.Column(db.Integer,default=0)

    def __init__(self):
        id=str(uuid.uuid1())
    def __repr__(self, *args, **kwargs):
        return '<Menu %s>'%self.name


