import os,sys
# append xbysite package to python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_security.utils import encrypt_password
from app import app
from app.extensions import db
from app.model.userrole import Role,user_datastore
import celery
from celery.bin import worker
from celery.bin import beat
from app import config
from multiprocessing import Process

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

def run_beat(application):
    c_beat=beat.beat(app=application)
    c_beat.run(loglevel='INFO')
def run_work(application):
    c_worker = worker.worker(app=application)
    c_worker.run(loglevel='INFO')

@manager.command
def startwork():
    '''
    act like 
    nohup celery app.util.tasks.celery_app beat &
    nohup celery -A app.util.tasks.celery_app worker &
    '''
    from app.util import  tasks
    application = celery.current_app._get_current_object()
    #在有beat scheduler时必须同时存在beat和worker进程，否则都无法正常工作。
    pbeat=Process(target=run_beat,args=(application,))
    pwork=Process(target=run_work,args=(application,))
    pbeat.start()
    pwork.start()    

@manager.command
def run():
    app.run()

if __name__ == "__main__":
    manager.run()