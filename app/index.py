from datetime import timedelta
import threading

from flask import current_app, jsonify,g,session
from flask_login import user_logged_out
from flask_security import url_for_security

from app import  app
from flask import render_template, redirect, request, flash, url_for, abort
import logging as log

from app import config
from app.views.pages import post_get
from app.util import exceptions,globalshare
from app.util.utilRedis import redis_decode_client as redis
from app.factory import db

session_ip_prefix='session_ip_'

@user_logged_out.connect_via(app)
def logoutSignalHandler(sender,user):
    session['login_retry']=0

    ip=request.headers['X-Real-IP'] or request.headers['Remote_Addr']
    redis.delete(session_ip_prefix+ip)

@app.context_processor
def inject_global_args():
    return dict(**globalshare.get_g_share())

@app.before_request
def before_request():
    #flask sessions expire once you close the browser unless you have a permanent session
    session.permanent = True
    #By default in Flask, permanent_session_lifetime is set to 31 days.
    app.permanent_session_lifetime = timedelta(minutes=30)
    max_login_retry=5

    ip=request.headers['X-Real-IP'] or request.headers['Remote_Addr']
    if (not getattr(g.identity,'user',None)) and request.path==url_for_security('login'):
        if request.method=='POST' and request.form['password']:
            login_retry=session.get('login_retry',0)+1
            session['login_retry'] = login_retry
            #使用redis来限制ip登录限制
            key=session_ip_prefix+ip
            with redis.pipeline() as pipe:
                pipe.incr(key).expire(key,2*3600).execute()
            #print(type(redis.get(key)))
            ip_retry_count=int(redis.get(key))
            
        
            if login_retry>max_login_retry or ip_retry_count>max_login_retry:
                return render_template('hintInfo.html',msg='登录次数超出限制,请2小时后重试')

    
    log.info(ip+" enter into "+request.path or ''+" for "+request.endpoint or ''+" of http method:"+request.method)

@app.errorhandler(exceptions.ArgsErrorException)
def argsErrorHandle(e):
    if request.is_xhr:
        return jsonify({'status':'fail','msg':e.msg})
    flash(e.msg,'danger')
    return render_template('hintInfo.html')

@app.after_request
def after_clean(resp,*args,**kwargs):
    db.session.commit()
    return resp
@app.teardown_request
def dbsession_clean(exception=None):
    try:
        db.session.remove()
    finally:
        pass



@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    # flash('这是首页', 'success')
    return post_get('home')
    #return render_template('home.html', title="xbynet平台首页")
