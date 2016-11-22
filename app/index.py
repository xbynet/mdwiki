from app import  app
from flask import render_template, redirect, request, flash, url_for, abort
import logging as log
from app.views.pages import post_get


@app.context_processor
def inject_global_args():
    return app.config['G_SHARE']


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    # flash('这是首页', 'success')
    return post_get('home')
    #return render_template('home.html', title="xbynet平台首页")
