from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, HiddenField
from wtforms.validators import DataRequired
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import util

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