from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, HiddenField
from wtforms.validators import DataRequired, StopValidation,Length,ValidationError
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import util
from flask_security import  LoginForm as SecLoginForm

class CaptchaValid(object):
    def __init__(self,message=None):
        self.message=message

    def verify_captcha(self,code):
        captchaCode = session.get('captcha', None)
        if not captchaCode or not code:
            return False
        if captchaCode.lower()==code.lower():
            return True
        return False

    def __call__(self, form, field):
        if  not self.verify_captcha(field.data):
            if self.message is None:
                message = field.gettext('验证码错误')
            else:
                message = self.message
            #field.errors[:] = []
            raise ValidationError(message)


class LoginForm(SecLoginForm):
    code=StringField('验证码',validators=[CaptchaValid("验证码无效")])

class SidebarForm(FlaskForm):
    content=TextAreaField('内容',validators=[DataRequired()])

class UserForm(FlaskForm):
    pass

class UploadForm(FlaskForm):
    __allowed_exts=['jpg','jpeg','png','gif','bmp','zip','docx','pdf']
    file=FileField('file',validators=[
        FileRequired(),FileAllowed(__allowed_exts,'file type not allowed')
        ]);

class PostForm(FlaskForm):
    title=StringField('标题',validators=[DataRequired()])
    content=TextAreaField('内容',validators=[DataRequired()])
    tags=StringField('tags')
    location=HiddenField('location',validators=[DataRequired()])
    createAt=HiddenField('createAt',default=util.getNowFmtDate())
    modifyAt=HiddenField('createAt',default=util.getNowFmtDate())
    fileModifyAt=HiddenField('fileModifyAt',default=util.getNowFmtDate())