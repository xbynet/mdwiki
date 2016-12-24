from flask import Flask
from flask_wtf import CsrfProtect
from redis import StrictRedis

from app.extensions import db,babel,moment,cache,security,mail
from .sessions import RedisSessionInterface
from app.util import utilRedis 
def create_app():
    from app import config
    app = Flask(__name__)
    app.config.from_object(config)
    #set server-side session if redis is valid
    if utilRedis.isValid():
        app.session_interface=RedisSessionInterface(redis=utilRedis.redis_pickle_client)
    # csrf ajax
    CsrfProtect(app)

    db.init_app(app)
    babel.init_app(app)
    moment.init_app(app)
    cache.init_app(app)
    mail.init_app(app)



    return app
