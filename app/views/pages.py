import os
from flask import Blueprint,render_template,redirect,request,flash,url_for,abort,current_app, jsonify
import json,re

from flask import make_response
from flask_login import current_user,login_required
from sqlalchemy.orm import joinedload_all

from app.views.forms import PostForm
from .import forms
from app.extensions import security, db
from app import util
import markdown
import logging as log
from datetime import datetime
from app.model.post import Post, Tag
from app.model.userrole import  User
from app.model import vo
from app.util import searchutil,utilpost
from app.util.utilRedis import redis_decode_client as redis
import bleach


pages=Blueprint('pages',__name__,url_prefix='/pages')

# @pages.route('/',methods=['GET'])
# def page_index():
    # return render_template('home.html')

@pages.route('/<path:path>',methods=['GET'])
def post_get(path):
    checked,path=util.checkPostLocation(path)
    if not checked:
        flash("路径参数错误",'danger')
        return render_template('hintInfo.html')
    else:
        abspath=os.path.join(current_app.config['PAGE_DIR'],path)+".md"
        if not os.path.exists(abspath):
            flash("页面不存在!",'danger')
            return render_template('hintInfo.html',canCreate=True,location=path)
        else:
            # with open(abspath,encoding='UTF-8') as f:
            #     content=f.read()
            # #title=content.split('\n\n',1)[0]
            # #content=content.split('\n\n',1)[1]
            # md_ext=util.Constant.md_ext
            # md=markdown.Markdown(output_format='html5',encoding='utf-8',extensions=md_ext)
            # html=util.html_clean(md.convert(content))
            #
            # toc=md.toc
            # meta=md.Meta
            html,toc,meta=utilpost.get_post_content(abspath)
            log.debug('meta %s' % meta)
            post=Post.query.get(path)
            if not post:
                post=Post(location=path)
            # user=User.query.get(post.userId)
            tagNames=[]
            if post.tags:
                tagNames=[tag.name for tag in post.tags]
            return render_template('page.html',content=html,toc=toc,title=meta.get('title',' ')[0],post=post,author=meta.get('author',' ')[0] ,meta=meta,tagNames=tagNames)

        # dirPath=path.split('/')[:-1]
        # filename=path.split('/')[-1]
        # if not os.path.exists(dirPath):
        #     os.makedirs(os.path.jodirPath)
@pages.route('/new/<path:path>',methods=['GET'])
@login_required
def post_new(path):
    checked,path=util.checkPostLocation(path)
    if not checked:
        flash("路径参数错误",'danger')
        return render_template('hintInfo.html')
    else:
        if utilpost.isPostLocked(path):
            flash("文章已被锁定,其他人正在编辑,您暂时无法编辑.")
            return render_template('hintInfo.html')

        utilpost.createPostLock(path)
        
        abspath=os.path.join(current_app.config['PAGE_DIR'],path)+".md"
        if not os.path.exists(abspath):
            form=PostForm()
            form.location.data=path
            flash('文章不存在，新建文章','info')
            return render_template('editor.html',title='新建文章',action=url_for('.post_save'),form=form,isPost=True)

@pages.route('/edit/<path:path>',methods=['GET'])
@login_required
def post_edit(path):
    path=util.urlDirPathFormat(path)
    abspath=os.path.join(current_app.config['PAGE_DIR'],path.replace('/',os.sep))+".md"
    if not os.path.exists(abspath):
        flash("文章不存在",'warning')
        return render_template('hintInfo.html')
    isAdmin=util.checkAdmin()

    post=Post.query.filter_by(location=path).first()

    if post and post.userId!=str(current_user.id) and (not isAdmin):
        flash("您没有权限编辑此文章!",'warning')
        return render_template('hintInfo.html')

    if utilpost.isPostLocked(path):
        flash("文章已被锁定，您暂时无权编辑")
        return render_template('hintInfo.html')
    utilpost.createPostLock(path)

    with open(abspath,encoding='UTF-8') as f:
        content=f.read()
            # print('fcontent'+fcontent)
            # form.content.data=fcontent
    meta = content.split('\n\n', 1)[0]
    meta=util.parsePostMeta(meta) # a dict
    content = content.split('\n\n', 1)[1]

    tags=''
    location=path

    if post:
        tags=','.join([t.name for t in post.tags])
        location = post.location

    fileModifyAt = datetime.fromtimestamp(os.stat(abspath).st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    form=PostForm(title=meta.get('title',''),content=content,
        location=location,tags=tags,
        createAt=meta.get('createAt',''),modifyAt=meta.get('modifyAt',' '),fileModifyAt=fileModifyAt)

    return render_template('editor.html',isPost=True,action=url_for('.post_save'),form=form)

@pages.route('/save',methods=['POST'])
@login_required
def post_save():
    form=PostForm()
    if form.validate_on_submit():
        checked,location=util.checkPostLocation(form.location.data)
        if not checked:
            flash('文章地址不合法', 'danger')
            return render_template('hintInfo.html')

        postExist=os.path.exists(util.getAbsPostPath(location))
        post=Post.query.filter_by(location=location).first()
        isAdmin=util.checkAdmin()

        isNew=True if not post else False
        if isNew and postExist and not isAdmin:
            flash("文章早已存在,您没有权限操作",'info')
            return redirect(url_for('.post_get',path=location))

        meta=dict(title=form.title.data,author=current_user.username or current_user.email,
            createAt=form.createAt.data,location=location
            ,modifyAt=util.getNowFmtDate())

        if isNew:
            meta['createAt']=util.getNowFmtDate()
            post=Post()
            post.location = location
            post.userId = current_user.id
            db.session.add(post)
            # else:
            #     flash('error location for post!','danger')
            #     return
        abspath=util.getAbsPostPath(post.location)
        if(form.fileModifyAt.data) and os.path.exists(abspath):
            orginModifyAt=datetime.fromtimestamp(os.stat(abspath).st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            #如果文件修改时间对不上，说明文件已经被修改过了
            if form.fileModifyAt.data!=orginModifyAt:
                flash("保存失败，在您编辑文章过程中，文件已经被修改过了!")
                return render_template('hintInfo.html')

        tags=form.tags.data.lower().split(',')
        tagsList=[]
        if isinstance(tags,list):
            for tagStr in tags:
                tagObj=Tag.query.filter_by(name=tagStr).first()
                if not tagObj:
                    # db.session.add(Tag(tagStr))
                    tagsList.append(Tag(tagStr))
                else:
                    # db.session.add(tagObj)
                    tagsList.append(tagObj)
        else:
            tagObj = Tag.query.filter_by(name=tags[0]).first()
            if not tagObj:
                # db.session.add(Tag(tagStr))
                tagsList.append(Tag(tags[0]))
            else:
                # db.session.add(tagObj)
                tagsList.append(tagObj)

        #post=db.session.merge(post)
        #print(post in db.session)
        post.tags=tagsList


        abspath=util.getAbsPostPath(post.location)

        if post.location.find(os.sep)>0:
            dir=abspath.rsplit(os.sep,1)[0]

            if not os.path.exists(dir):
                os.makedirs(dir)
        with open(abspath,'w+',encoding='UTF-8') as f:
            # 这一步很坑，一定要去掉\r，否则每次编辑器显示都会多出空行
            content = form.content.data.replace('\r', '')
            # print(meta)
            f.write(util.fmtPostMeta(meta)+content)
        postvo=vo.SearchPostVo(content=content,summary=content[:100],**meta)
        if isNew:
            searchutil.indexDocument([postvo])
        else:
            searchutil.updateDocument([postvo])

        utilpost.releasePostLock(post.location)
        utilpost.delete_post_cache(abspath)
        return redirect(url_for('.post_get',path=post.location))

    flash('保存失败', 'danger')
    return render_template('hintInfo.html')

@pages.route('/delete/<path:path>',methods=['GET','POST'])
@login_required
def post_delete(path):
    isAdmin=util.checkAdmin()
    if isAdmin:
        post=Post.query.filter_by(location=path).first()
    else:
        post=Post.query.filter_by(location=path,userId=str(current_user.id)).first()

    path=util.urlDirPathFormat(path)
    abspath=util.getAbsPostPath(path)
    if post or os.path.exists(abspath):
        if post:
            log.debug(post.location+post.userId)
            db.session.delete(post)

        if os.path.exists(abspath):
            os.remove(abspath)

        term=dict(fieldName='location',text=path)
        try:
            searchutil.deleteDocument([term])
            #db.session.commit()
            utilpost.delete_post_cache(abspath)
            flash("删除成功！", "success")
        except AttributeError as e:
            flash("发生内部错误 %s" % str(e),'danger')
    else:
        flash("文章不存在或无权限编辑!","warning")
    return render_template('hintInfo.html')

@pages.route("/list/<string:tagName>/<int:curNum>")
def     postlistByTag(tagName,curNum):
    if not tagName.strip() or not curNum or curNum<1:
        flash("参数错误!","warning")
        return render_template('hintInfo.html')
    paginate=Post.query.filter(Post.tags.any(name=tagName)).order_by(Post.location).paginate(curNum,15,False)
    cur_posts=paginate.items
    posts=list()
    for cur_post in cur_posts:
        abspath=util.getAbsPostPath(cur_post.location)
        if not os.path.exists(abspath):
            continue
        with open(abspath,'r',encoding='utf-8') as f:
            content=f.read()
            conSplit=content.split('\n\n',1)
            if len(conSplit)<2:
                metaStr=''
                postContent = conSplit[0]
            else:
                metaStr=conSplit[0]
                postContent= conSplit[1]
            meta=util.parsePostMeta(metaStr)
            summary=postContent[:200]
        posts.append({'location':cur_post.location,'title':meta['title'],'summary':summary,'meta':meta})
    return render_template('tagsPostList.html',tagName=tagName,paginate=paginate,posts=posts,curNum=curNum)


@pages.route("/tag/list")
def tagList():
    tags=Tag.query.all()
    return render_template('tags.html',tags=tags)

@pages.route("/search")
def searchDef():
    return search(1)
    
@pages.route("/search/<int:curPage>",methods=["GET","POST"])
def search(curPage):
    keyword=request.args.get('keyword','')
    if not keyword:
        flash("参数错误!","warning")
        return render_template('hintInfo.html')
    if not curPage:
        curPage=int(request.args.get('curPage',1))
    pagelen=int(request.args.get("pagelen",30))

    results=searchutil.searchPage(keyword,curPage,pagelen)

    return render_template('searchResult.html',keyword=keyword,results=results)

@pages.route('/rebuildIndex')
@login_required
def rebuildIndex():
    searchutil.reBuildIndex()
    return jsonify({'status':'ok'})


@pages.route('/checkLock')
@login_required
def checkPostLock():
    """文件锁定失效由两个redis string变量控制utilpost.getPostLockKey返回的key0,key1
    key0表示最大允许失效时间，key1表示临时允许失效时间，结合两者可以越过无法处理浏览器关闭、刷新等事件的问题。
    key1设定时长较短为60s，浏览器轮询服务端来不断刷新过期时间，以确保锁定持续。文章编辑也仅会检查该变量是否存在，存在则表示锁定。
    如果key1不存在，则不会去检查key0，这时处于没有锁定状态，但是如果key1不存在，那么也将删除key0，因为这时已超出最大允许编辑时间。
    Returns:
        TYPE: Description
    """
    if not request.args.get('location'):
        return jsonify({'status':'fail'})

    key0,key1=utilpost.getPostLockKey(request.args.get('location'))

    if redis.get(key0):
        redis.expire(key1,60)
        return jsonify({'status':'ok'})
    else:
        #如果失效总时间过期，那么删除临时失效时间，这时文章锁定真正失效。
        redis.delete(key1)
        return jsonify({'status':'unlock'})

