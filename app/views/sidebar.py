from flask_login import login_required
from flask_security import roles_accepted
from flask_security import roles_required
from flask.views import MethodView
from flask import  render_template,url_for,redirect,request
import os
from .forms import SidebarForm
from . import views
from app.util import Constant,SidebarInit


@views.route('/sidebar/edit')
@login_required
# @roles_accepted('admin', 'editor')
def editSidebar():
    form=SidebarForm()
    fcontent=''
    if os.path.exists(Constant.SIDEBAR_PATH):
        with open(Constant.SIDEBAR_PATH,encoding='UTF-8') as f:
            fcontent=f.read()
            # print('fcontent'+fcontent)
            form.content.data=fcontent
    return render_template('editor.html',isSidebar=True,action=url_for('.saveSidebar'),form=form)

@views.route('/sidebar/save',methods=['POST'])
@login_required
# @roles_accepted('admin', 'editor')
def saveSidebar():
    form=SidebarForm()
    if form.validate_on_submit():
        with open(Constant.SIDEBAR_PATH,'w',encoding='UTF-8') as f:
            #这一步很坑，一定要去掉\r，否则每次编辑器显示都会多出空行
            content=form.content.data.replace('\r','')
            #print(content)
            f.write(content)
            SidebarInit.initSidebarWithContent(content)

        return redirect(url_for('home'))
    return render_template('editor.html',isSidebar=True,action=url_for('.saveSidebar'),form=form)
