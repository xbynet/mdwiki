import json

import logging.config
import os,sys
from logging.handlers import SMTPHandler

from flask_security import Security

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import config
from app.factory import create_app


from app.views.forms import LoginForm

app=create_app()


# Setup Flask-Security

from app.model.userrole import user_datastore
security = Security(app, user_datastore,login_form=LoginForm)
# security.init_app(app, user_datastore)
security.login_manager.login_message_category = 'danger'
security.login_manager.login_message = '请登录'

###########################
# init logging
###########################
if (os.path.exists(config.LOG_CFG_FILE)):
    with open(config.LOG_CFG_FILE, 'r') as f:
        cfg = json.load(f)
        logging.config.dictConfig(cfg)
        mail_handler = SMTPHandler((config.MAIL_SERVER, config.MAIL_PORT), config.MAIL_DEFAULT_SENDER,
                                   config.LOG_MAIL_RECIEVER, "xbysite程序出现严重错误，请及时修复",
                                   (config.MAIL_USERNAME, config.MAIL_PASSWORD), 'SSL')
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
else:
    logging.basicConfig(level='INFO')

with app.app_context():
    from app import util
    # 初始化侧边栏数据
    util.SidebarInit.initSidebar()

from . import index
from .views import all_blueprint
for bp in all_blueprint:
    app.register_blueprint(bp)

#logging.warn('api_key %s' % os.environ.get('aliyun_api_key', ''))
#
from app.util import tasks
