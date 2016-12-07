from flask import render_template
from . import views
from app.factory import cache


@views.app_errorhandler(404)
@cache.cached(key_prefix='404')
def page_not_found(e):
    return render_template('404.html'),404


@views.app_errorhandler(401)
@cache.cached(timeout=36000,key_prefix='401')
def unathorized_error(e):
    return render_template('401.html'),401


@views.app_errorhandler(405)
@cache.cached(timeout=36000,key_prefix='405')
def unathorized_method_error(e):
    return  render_template('405.html'),405