"""Summary
"""
import os
import sys
import shutil
import re
import tarfile
import platform
import json
import threading 
import  logging as log

import markdown
from celery import Celery
from flask import current_app
from flask_login import current_user

from datetime import datetime
import bleach
from app import config
from . import Constant,globalshare

class SidebarInit():
    """Summary
    """
    lock = threading.Lock()

    @classmethod
    def initSidebar(cls):
        """Summary
        Returns:
            TYPE: Description
        """

        with open(Constant.SIDEBAR_PATH,'r',encoding='UTF-8') as f:
            cls.initSidebarWithContent(f.read())

    @classmethod
    def initSidebarWithContent(cls,content):
        sidebar = []
        for line in content.split("\n"):
            # line=f.readline() # #连接:名字:图标名，形式
            # print(line)
            if line.startswith('## ') and len(line.strip()) > 2:
                tmp = cls.__analyzeLine(line, '## ')

                if sidebar[-1].get('childrens') is None:
                    sidebar[-1]['childrens'] = list()
                sidebar[-1]['childrens'].append(
                    {'link': tmp[0], 'name': tmp[1], 'icon': tmp[2], 'type': 1, 'target': tmp[3]})
            elif line.startswith('# ') and len(line.strip()) > 1:
                tmp = cls.__analyzeLine(line, '# ')
                sidebar.append({'link': tmp[0], 'name': tmp[1], 'icon': tmp[2], 'type': 0, 'target': tmp[3]})
        # print(sidebar)
        # print(app.config['G_SHARE']['sidebar'])

        with cls.lock:

            globalshare.set_sidebar(sidebar)
            # config.G_SHARE['sidebar'] = sidebar

    @classmethod
    def __analyzeLine(cls,line,flag):
        """Summary
        
        Args:
            line (TYPE): Description
            flag (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        line=line.strip()
        default_icon='th-list'
        is_http=line.startswith(flag+"http://") or line.startswith(flag+"https://")
        if is_http:
            default_icon='share'
        spliteCount=2
        if line.count(':')==2:
            if is_http:
                spliteCount=1
        elif line.count(':')==1:
            if is_http:
                spliteCount=0
        tmp = line.replace(flag, '').rsplit(':',spliteCount)
        if len(tmp) == 1:
            tmp.append(tmp[0].strip())
            tmp.append(default_icon)
        elif len(tmp) == 2:
            tmp.append(default_icon)
        tmp.append('_blank' if is_http else '')
        return tmp

def walkDirGenDataUrl(subdir,urllist=[],pathlist=[]):
    """Summary
    
    Args:
        subdir (TYPE): Description
        urllist (list, optional): Description
        pathlist (list, optional): Description
    
    Returns:
        TYPE: Description
    """
    BASE=config.DATA_DIR
    dirname=BASE+os.sep+subdir
    if not os.path.exists(dirname):
        return
    for path,dirs,files in os.walk(dirname):
        for name in files:
            fullpath=os.path.join(path,name)
            pathlist.append(fullpath)
            urllist.append(fullpath[len(config.DATA_DIR.rsplit(os.sep,1)[0]):])  
        for dirfile in dirs:
            if dirfile=='.' or dirfile=='..':
                continue
            fullpath=os.path.join(path,dirfile)


def urlDirPathFormat(path):
    """Summary
    
    Args:
        path (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    path = path.strip()
    path = path.replace('..', '')
    path = path.replace('./', '/')
    return path

def checkPostLocation(location):
    """检查文章location参数是否合法
    
    Args:
        location (str)
    
    Returns:
        tuple: 返回一个包含两个值的元组。如(True,location)
    """
    exclude=['save','edit','delete']
    if location in exclude:
        return False,location
    location=urlDirPathFormat(location)
    location=location.replace('/', os.sep).replace('\\', os.sep)
    if location.strip()=='':
        return False,location
    while location.startswith(os.sep):
        location=location[1:]
        if location.strip()=='':
            return (False,location)

    return True,location


def fmtPostMeta(metaDict):
    """Summary
    
    Args:
        metaDict (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    metaStr=''
    for key,value in metaDict.items():
        metaStr+=str(key)+":"+value.replace('\r','').replace('\n','')+'\n'
    return metaStr+'\n'
def parsePostMeta(metaStr):
    """Summary
    
    Args:
        metaStr (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    lines=metaStr.split('\n')
    resMeta=dict([tuple([line.split(':')[0],':'.join(line.split(':')[1:])] if len(line.split(':'))>2 else line.split(':')) for line in lines])
    return resMeta

def getNowFmtDate():
    """Summary
    
    Returns:
        TYPE: Description
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getAbsPostPath(location):
    """Summary
    
    Args:
        location (TYPE): Description
    
    Returns:
        TYPE: Description
    """

 #   with current_app.app_context():
    abspath=os.path.join(config.PAGE_DIR,location.replace('/',os.sep))+".md"

    return abspath
def getAbsDataItemPath(path):
    """Summary
    
    Args:
        path (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    with current_app.app_context():
        abspath=os.path.join(current_app.config['DATA_DIR'],path)
    return abspath

def objToDict(obj):
    """convert obj attr to dict
    
    Args:
        obj (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    objDict=dict((name, getattr(obj, name)) for name in dir(obj)   
       if not name.startswith('__')  and not callable(name))
    return objDict 

def checkAdmin():
    isAdmin=False
    if 'admin' in [ role.name for role in current_user.roles]:
        isAdmin=True
    return isAdmin

def checkOS():
    """check operator system
    
    Returns:
        str: windows or linux
    """
    return platform.system().lower()







