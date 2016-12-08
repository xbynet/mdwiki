import os,uuid,logging
from .forms import UploadForm
from . import views
from app import config
from flask import request,render_template,redirect,url_for,current_app,jsonify,send_file,session
from werkzeug.utils import secure_filename
from app.util import captcha
from io import BytesIO

UPLOAD_DIR=os.path.join(config.DATA_DIR,'upload')

@views.route('/upload',methods=['POST'])
def upload():
    form=UploadForm()
    res=dict()
    if form.validate_on_submit():
        filename=secure_filename(form.file.data.filename)
        logging.info('upload file %s' % filename)
        filename=str(uuid.uuid1())+'.'+filename.split('.')[-1]
        logging.debug(os.path.join(UPLOAD_DIR,filename))
        form.file.data.save(os.path.join(current_app.config['DATA_DIR'],'upload',filename))
        res['msg']='uploaded'
        res['filename']=filename
        res['link']=current_app.config['DOWNLOAD_URL_PREFIX']+filename
    else:
        res['msg']='failed'
        res['link']=''
        res['filename'] =''
    return jsonify(res)



@views.route('/captcha')
def getCaptcha():
    def serve_pil_image(pil_img):
        img_io = BytesIO()
        pil_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png',cache_timeout=0)
    code_img=captcha.createCaptcha()
    session['captcha']=code_img[1]
    return serve_pil_image(code_img[0])