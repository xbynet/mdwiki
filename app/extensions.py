from flask.ext.security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
# from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_cache import Cache
# from flask_restful import Resource, Api
from flask_babel import Babel
# from flask_security import Security
from flask_mail import Mail

babel = Babel()
# api=Api()
db = SQLAlchemy()
# Bootstrap()
moment = Moment()
cache = Cache()
security = Security()
mail = Mail()


