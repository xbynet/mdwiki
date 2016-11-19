import os
from flask import current_app

from datetime import datetime
from . import Constant
from app import app


class SidebarInit():

    @classmethod
    def initSidebar(cls,app):
        sidebar=app.config['G_SHARE']['sidebar']=[]
        with open(Constant.SIDEBAR_PATH,'r',encoding='UTF-8') as f:
            for line in f:
                # line=f.readline() # #连接:名字:图标名，形式
                # print(line)
                if line.startswith('## ') and len(line.strip())>2:
                    tmp = cls.__analyzeLine(line,'## ')

                    if sidebar[-1].get('childrens') is None :
                        sidebar[-1]['childrens']=list()
                    sidebar[-1]['childrens'].append({'link':tmp[0],'name':tmp[1],'icon':tmp[2],'type':1,'target':tmp[3]})
                elif line.startswith('# ') and len(line.strip())>1:
                    tmp=cls.__analyzeLine(line,'# ')
                    sidebar.append({'link':tmp[0],'name':tmp[1],'icon':tmp[2],'type':0,'target':tmp[3]})
            # print(sidebar)
            # print(app.config['G_SHARE']['sidebar'])


    @classmethod
    def __analyzeLine(cls,line,flag):
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

def urlDirPathFormat(path):
    path = path.strip()
    path = path.replace('..', '')
    path = path.replace('./', '/')
    return path

def checkPostLocation(location):
    """检查文章location参数是否合法
    Args:
        location (str): 
    
    Returns:
        tuple:返回一个包含两个值的元组。如(True,location)
    """
    exclude=['save','edit','delete']
    if location in exclude:
        return False,location
    location=urlDirPathFormat(location)
    if location.strip()=='':
        return False,location
    if location.startswith('/'):
        location=location[1:]
        if location.strip()=='':
            return (False,location)

    return True,location


def fmtPostMeta(metaDict):
    metaStr=''
    for key,value in metaDict.items():
        metaStr+=str(key)+":"+value.replace('\r','').replace('\n','')+'\n'
    return metaStr+'\n'
def parsePostMeta(metaStr):
    lines=metaStr.split('\n')
    resMeta=dict([tuple([line.split(':')[0],':'.join(line.split(':')[1:])] if len(line.split(':'))>2 else line.split(':')) for line in lines])
    return resMeta

def getNowFmtDate():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getAbsPostPath(location):
    with app.app_context():
        abspath=os.path.join(current_app.config['PAGE_DIR'],location.replace('/',os.sep))+".md"
    return abspath
