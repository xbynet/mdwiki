import os

from flask import Blueprint, jsonify
from flask import render_template
from flask import request
from flask_login import login_required

from app import util
from app.util.exceptions import *
from app.util.backup import AliyunOSS
from app import config

admin=Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/manage')
@login_required
def manage():
    infos=backupinfo()
    return render_template('manage.html',title='xbynet后台管理',bakData=infos)

@admin.route('/image/index')
@login_required
def imageIndex():
    topPathlist=['upload','upload_bak','dokuwiki']
    path=request.args.get('path','upload')
    if path:
        isValid,path=util.checkPostLocation(path)
        if not isValid:
            raise ArgsErrorException('路径参数错误')
    imgDir=util.getAbsDataItemPath(path)
    if not (os.path.exists(imgDir) and os.path.isdir(imgDir)):
        raise ArgsErrorException('路径参数错误')

    images=list()
    dirs=list()
    curPage=int(request.args.get('curPage',1))
    pageSize=int(request.args.get('pageSize',10))
    for filename in os.listdir(imgDir):
        if os.path.isdir(imgDir+os.sep+filename):
            tdir=dict(path=path+os.sep+filename,name=filename,link='/data/'+path+'/'+filename)
            dirs.append(tdir)
            continue
        if os.path.splitext(filename)[1][1:] in ['png','jpg','bmp','gif','jpeg']:
            img=dict(path=path+os.sep+filename,link='/data/'+path+'/'+filename)
            images.append(img)
    if request.is_xhr:
        return jsonify(images[(curPage-1)*pageSize:curPage*pageSize])
    else:
        return render_template('picManager.html',topPathlist=topPathlist,breadcrumbs=path.replace('/',os.sep).split(os.sep),path=path,dirs=dirs,images=images[:10],maxPage=len(images)//pageSize+1)

@admin.route('/image/delete',methods=['GET','POST'])
@login_required
def imageDelete():
    if request.args.get('path',''):
        path=util.urlDirPathFormat(request.args.get('path',''))
        path=util.getAbsDataItemPath(path)
        if os.path.exists(path):
            os.remove(path)
    return jsonify({'status':'ok'})

@admin.route('/backup/delete/<string:key>')
@login_required
def backupDelete(key):
    if not key:
        raise ArgsErrorException('参数错误')
    oss=AliyunOSS(**config.oss)
    oss.deleteFile(key)
    return jsonify({'status':'ok','msg':'删除成功'})
@admin.route('/backup/download/<string:key>')
@login_required
def backupDownload(key):
    if not key:
        raise ArgsErrorException('参数错误')
    oss=AliyunOSS(**config.oss)
    url=oss.getDownloadUrl(key)
    return jsonify({'status':'ok','url':url})

def backupinfo():
    oss = AliyunOSS(**config.oss)
    lists=oss.listFiles()
    return lists
