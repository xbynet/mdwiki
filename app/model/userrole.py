from flask.ext.security import SQLAlchemyUserDatastore

from app.extensions import db
from flask_security import  UserMixin, RoleMixin



roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description=''):
        self.name = name
        self.description = description

        def __repr__(self):
            return "<Role %s--%s>" % (self.name, self.description)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    # 如果你配置了SECURITY_CONFIRMABLE=True，那么你的User模型需要添加以下字段：
    confirmed_at = db.Column(db.DateTime())
    # 如果你配置了SECURITY_TRACKABLE=True，那么你的User模型需要添加以下字段：
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))
    login_count = db.Column(db.BigInteger())

    def __repr__(self):
        return "<User %s--%s>" % self.name

user_datastore = SQLAlchemyUserDatastore(db, User, Role)