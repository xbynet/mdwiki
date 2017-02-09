from flask import render_template
from flask.helpers import flash

from app.factory import cache

from . import views


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

@views.app_errorhandler(400)
def page_400():
    flash('发生未知错误,通常情况下可能是您的会话已经失效!')
    return render_template('hintInfo.html')