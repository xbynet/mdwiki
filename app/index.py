from . import app
from flask import render_template, redirect, request, flash, url_for, abort
import logging as log



@app.context_processor
def inject_global_args():
    log.debug('22222222')
    return app.config['G_SHARE']


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    log.debug(1111111)
    flash('这是首页', 'success')
    return render_template('home.html', title="xbynet平台首页")
