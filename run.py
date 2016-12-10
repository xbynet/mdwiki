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

@manager.option('-n','--name',help='username',required=True)
@manager.option('-e','--email',help='email',required=True)
@manager.option('-p','--password',help='password',required=True)
def init_admin(name,email,password):
    if name=='' or email=='' or password=='' or len(password)<6:
        print('创建失败，相关参数为空，或密码长度小于6')
        return
    user=user_datastore.find_user(username=name,email=email)
    if user is None:
        user=user_datastore.create_user(username=name,email=email,password=encrypt_password(password))
    
    role=user_datastore.find_or_create_role('admin',description='administrator role')

    if user.roles is  None:
        user.roles=[]
    user.roles.append(role)
    db.session.commit()

@manager.option('-n','--name',help='username',required=True)
@manager.option('-e','--email',help='email',required=True)
@manager.option('-p','--password',help='password',required=True)
@manager.option('-r','--roles',nargs='*',default=['editor'],help='roles separator by space')
@manager.option('-d','--rolesDesc',nargs='*',default=['editor'],help='rolesdesc separator by space')
def create_user(name,email,password,roles,rolesDesc):
    #print('--------------------------------%s' % type(roles))
    if len(roles)!=len(rolesDesc):
        raise Exception('roles len not equals rolesDesc len')
    if name=='' or email=='' or password=='' or len(password)<6:
        print('创建失败，相关参数为空，或密码长度小于6')
        return
    user=user_datastore.find_user(username=name,email=email)
    if user is None:
        user=user_datastore.create_user(username=name,email=email,password=encrypt_password(password))
    rolelist=[]

    for index,rolename in enumerate(roles):
        role=user_datastore.find_or_create_role(rolename,description=rolesDesc[index])
        rolelist.append(role)
    user.roles=rolelist
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
    nohup celery beat -A app.util.tasks.celery_app  -f celery.beat.log -l info &
    nohup celery worker -A app.util.tasks.celery_app  -f celery.worker.log -l info &
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