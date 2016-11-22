import os,sys
# append xbysite package to python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_security.utils import encrypt_password
from app import app
from app.extensions import db
from app.model.userrole import Role,user_datastore


migrate=Migrate(app,db)
manager=Manager(app)
manager.add_command('db',MigrateCommand)

@manager.command
def create_db():
	db.create_all()

@manager.command
def init_admin():
    user=user_datastore.create_user(email='xby@xbynet.net',password=encrypt_password("1"))
    role=Role('admin','administrator role')
    if user.roles is  None:
        user.roles=[]
    user.roles.append(role)
    db.session.commit()

@manager.command
def run():
    app.run()

if __name__ == "__main__":
    manager.run()