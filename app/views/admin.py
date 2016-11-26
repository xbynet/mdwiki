import os

from flask import Blueprint, jsonify
from flask import render_template
from flask import request
from flask_login import login_required

from app import util
from app.util.exceptions import *

admin=Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/manage')
@login_required
def manage():
    return render_template('manage.html')

@admin.route('/image/index')
@login_required
def imageIndex():
    topPathlist=['upload','dokuwiki']
    path='upload'
    if request.args.get('path',''):
        isValid,path=util.checkPostLocation(request.args.get('path',''))
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