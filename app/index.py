from flask import current_app, jsonify

from app import  app
from flask import render_template, redirect, request, flash, url_for, abort
import logging as log
from app.views.pages import post_get
from app.util import exceptions

@app.context_processor
def inject_global_args():
    return app.config['G_SHARE']

@app.before_request
def before_reuquest():
    log.info("enter into "+request.full_path or ''+" for "+request.endpoint or ''+" of http method:"+request.method)
@app.errorhandler(exceptions.ArgsErrorException)
def argsErrorHandle(e):
    if request.is_xhr:
        return jsonify({'status':'fail','msg':e.msg})
    flash(e.msg,'danger')
    return render_template('hintInfo.html')

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    # flash('这是首页', 'success')
    return post_get('home')
    #return render_template('home.html', title="xbynet平台首页")
