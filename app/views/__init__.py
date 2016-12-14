""" this is a BluePrint for views """
from flask import Blueprint
import  logging as log
import os
# from functools import wraps
# from app.extensions import db


# def route(app_or_sub,rule,**options):
#     def decorator(f):
#         @wraps(f)
#         def decorated_view(*args,**kwargs):
#             res=f(*args,**kwargs)
#             db.session.commit()
#             return res
#         endpoint = options.pop('endpoint', None)
#         app_or_sub.add_url_rule(rule, endpoint, decorated_view, **options)
#         return decorated_view
#     return decorator


######blueprints########################
views=Blueprint('views',__name__)
from .pages import pages as pages_blueprint
from .admin import admin as admin_blueprint
all_blueprint=[views,pages_blueprint,admin_blueprint]

from . import sidebar,errors,pages,admin,security,tags
