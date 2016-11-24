from flask import Flask
from flask_wtf import CsrfProtect
from app import config
from app.extensions import db,babel,moment,cache,security



def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # csrf ajax
    CsrfProtect(app)

    db.init_app(app)
    babel.init_app(app)
    moment.init_app(app)
    cache.init_app(app)




    #######Menu##############
    app.config['G_SHARE'] = \
        { \
            'title': config.APP_NAME, \
            'menus': [{'name': '标签', 'icon': 'tags', 'type': 0, 'link': '/pages/tag/list', 'active': ''}, \
                      {'name': '侧边栏', 'icon': 'tags', 'type': 0, 'link': '/sidebar/edit', 'active': ''}], \
            'sidebar': [] \
        }
    return app
