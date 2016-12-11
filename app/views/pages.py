import os
from flask import Blueprint,render_template,redirect,request,flash,url_for,abort,current_app, jsonify
import json,re

from flask import make_response
from flask_login import current_user,login_required

from app.views.forms import PostForm
from .import forms
from app.extensions import security, db
from app import util
import markdown
import logging as log
from app.model.post import Post, Tag
from app.model.userrole import  User
from app.model import vo
from app.util import searchutil
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
            with open(abspath,encoding='UTF-8') as f:
                content=f.read()
            #title=content.split('\n\n',1)[0]
            #content=content.split('\n\n',1)[1]
            md_ext=util.Constant.md_ext
            md=markdown.Markdown(output_format='html5',encoding='utf-8',extensions=md_ext)
            html=md.convert(content)

            toc=md.toc
            meta=md.Meta

            log.debug('meta %s' % meta)
            post=Post.query.get(path)
            if not post:
                post={'location':path}
            # user=User.query.get(post.userId)
            return render_template('page.html',content=html,toc=toc,title=meta.get('title',' ')[0],post=post,author=meta.get('author',' ')[0] ,meta=meta)

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
    form=PostForm(title=meta.get('title',''),content=content,
        location=location,tags=tags,
        createAt=meta.get('createAt',''),modifyAt=meta.get('modifyAt',' '))
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
            
            # else:
            #     flash('error location for post!','danger')
            #     return
        tags=form.tags.data.split(',')
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

        post.tags=tagsList
        if isNew:
            db.session.add(post)
        db.session.commit()

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
            db.session.commit()
            flash("删除成功！", "success")
        except AttributeError as e:
            flash("发生内部错误 %s" % str(e),'danger')
    else:
        flash("文章不存在或无权限编辑!","warning")
    return render_template('hintInfo.html')

@pages.route("/list/<string:tagName>/<int:curNum>")
def postlistByTag(tagName,curNum):
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
    return render_template('tagsPostList.html',tagName=tagName,paginate=paginate,posts=posts)


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