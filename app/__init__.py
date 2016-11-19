import os, sys, json
import logging
import logging.config
from logging.handlers import SMTPHandler
from . import config
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
# from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_cache import Cache
# from flask_restful import Resource, Api
from flask_babel import Babel
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

app = Flask(__name__)
app.config.from_object(config)

babel = Babel(app)
# api=Api(app)
db = SQLAlchemy(app)
# Bootstrap(app)
moment = Moment(app)
cache = Cache(app)
celery_app = config.make_celery(app)


#csrf ajax
CsrfProtect(app);
###########################
# init logging
###########################
if (os.path.exists(config.LOG_CFG_FILE)):
    with open(config.LOG_CFG_FILE, 'r') as f:
        cfg = json.load(f)
        logging.config.dictConfig(cfg)
        mail_handler = SMTPHandler((config.MAIL_SERVER, config.MAIL_PORT), config.MAIL_DEFAULT_SENDER,
                                   config.LOG_MAIL_RECIEVER, "xbysite程序出现严重错误，请及时修复",
                                   (config.MAIL_USERNAME, config.MAIL_PASSWORD), 'SSL')
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
else:
    logging.basicConfig(level='INFO')

###########################
# flask-security config
###########################
# Define models
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


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
security.login_manager.login_message_category = 'danger'
security.login_manager.login_message = '请登录'
from . import index
from . import views
from .views import all_blueprint

for bp in all_blueprint:
    app.register_blueprint(bp)
# map(app.register_blueprint,all_blueprint)
# app.config['G_SHARE'] = \
#     { \
#         'title': app.config['APP_NAME'], \
#         'menus': [{'name': 'posts', 'icon': 'th-list', 'type': 0, 'link': '#', 'active': ''}, \
#                   {'name': 'tags', 'icon': 'tags', 'type': 0, 'link': '#', 'active': ''}, \
#                   {'name': '侧边栏', 'icon': 'tags', 'type': 0, 'link': '/sidebar/edit', 'active': ''}], \
#         'sidebar': [] \
#         }

from . import util

# 初始化侧边栏数据
util.SidebarInit.initSidebar(app)
