import os
from datetime import datetime
import logging as log
from flask_login import current_user
from app import util
from app.util.utilRedis import redis_client as redis


def getPostLockKey(path):
    #文章锁定，默认30分钟
    key0='post:lock:%s' % path.replace('\\','/')
    #轮询锁定，用于辅助判断页面是否关闭以便释放锁
    key1='post:%s' % path.replace('\\','/')

    return key0,key1


def isPostLocked(path):
    key0,key1=getPostLockKey(path)
    key1Value=redis.get(key1)
    if (not key1Value) or key1Value.decode('utf-8') == current_user.email:
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
