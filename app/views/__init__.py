""" this is a BluePrint for views """
from flask import Blueprint
import  logging as log
import os


######blueprints########################
views=Blueprint('views',__name__)
from .pages import pages as pages_blueprint
from .admin import admin as admin_blueprint
all_blueprint=[views,pages_blueprint,admin_blueprint]

from . import sidebar,errors,pages,admin,security,tags
