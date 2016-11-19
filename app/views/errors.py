from flask import render_template
from . import views

@views.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@views.app_errorhandler(401)
def unathorized_error(e):
    return render_template('401.html'),401

@views.app_errorhandler(405)
def unathorized_method_error(e):
    return  render_template('405.html'),405