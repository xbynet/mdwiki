import json
import os
from datetime import datetime
import logging as log

import bleach
import markdown
from flask_login import current_user
from app import util
from app.util import Constant
from app.util.utilRedis import redis_decode_client as redis


def getPostLockKey(path):
    #文章锁定，默认30分钟
    key0='post:lock:%s' % path.replace('\\','/')
    #轮询锁定，用于辅助判断页面是否关闭以便释放锁
    key1='post:%s' % path.replace('\\','/')

    return key0,key1


def isPostLocked(path):
    key0,key1=getPostLockKey(path)
    key1Value=redis.get(key1)
    if (not key1Value) or key1Value == current_user.email:
        return False
    return True

def createPostLock(path):
    key0,key1=getPostLockKey(path)
    with redis.pipeline() as pipe:
        pipe.setex(key0,30*60,1).setex(key1,60,current_user.email).execute()

def releasePostLock(path):
    key0,key1=getPostLockKey(path)
    with redis.pipeline() as pipe:
        pipe.delete(key0,key1).execute()

def html_clean(htmlstr):
    tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul']
    tags.extend(['div','p','hr','br','pre','code','span','h1','h2','h3','h4','h5','del','dl','img','sub','sup','u',
                 'table','thead','tr','th','td','tbody','dd','caption','blockquote','section'])
    attributes = {'*':['class','id'],'a': ['href', 'title','target'],'img':['src','style','width','height']}
    return bleach.linkify(bleach.clean(htmlstr,tags=tags,attributes=attributes))



def get_post_content(abspath):

    key='post_get:%s' % abspath

    if redis.exists(key):
        alldict=redis.hgetall(key)
        html=alldict['html']
        toc=alldict['toc']
        meta=json.loads(alldict['meta'],encoding='utf-8')
        redis.expire(key,60*60*1)
        return html,toc,meta
    with open(abspath, encoding='UTF-8') as f:
        content = f.read()
    # title=content.split('\n\n',1)[0]
    # content=content.split('\n\n',1)[1]
    md_ext = Constant.md_ext
    md = markdown.Markdown(output_format='html5', encoding='utf-8', extensions=md_ext)
    html = html_clean(md.convert(content))


    toc = md.toc or ''
    meta = md.Meta or {}

    with redis.pipeline() as pipe:
        pipe.hmset(key,{'html':html,'toc':toc,'meta':json.dumps(meta)}).expire(key,60*60*1).execute()

    return html,toc,meta
def delete_post_cache(abspath):
    key='post_get:%s' % abspath
    redis.delete(key)