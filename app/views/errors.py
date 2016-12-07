from flask import render_template
from . import views
from app.factory import cache

@cache.cached(timeout=3600)
@views.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@cache.cached(timeout=3600)
@views.app_errorhandler(401)
def unathorized_error(e):
    return render_template('401.html'),401

@cache.cached(timeout=3600)
@views.app_errorhandler(405)
def unathorized_method_error(e):
    return  render_template('405.html'),405