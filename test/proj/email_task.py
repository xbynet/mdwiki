import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import hashlib
import time
from importlib import reload

from proj.main import celery_app
import celery
from celery.bin import beat,worker
from multiprocessing import Process
#sys.path.append(os.path.join(os.path.dirname(__file__), "./"))
 
@celery_app.task()
def do_email():
    print('begin to email')
    with open(r'C:\Users\taojw\Desktop\pywork\mdwiki\11.txt','a+') as f:
        f.write('1111\n')
    print('email complete')
 
@celery_app.task()
def do_email_new():
    print('begin to email new')
    time.sleep(1)
    with open(r'C:\Users\taojw\Desktop\pywork\mdwiki\11.txt','a+') as f:
        f.write('222\n')
    print('email new complete')

def run_beat(application):
    c_beat=beat.beat(app=application)

    c_beat.run(loglevel='DEBUG')
def run_work(application):
    c_worker = worker.worker(app=application)
    c_worker.run(loglevel='DEBUG')

if __name__ == '__main__':
    application = celery.current_app._get_current_object()

    #在有beat scheduler时必须同时存在beat和worker进程，否则都无法正常工作。
    pbeat=Process(target=run_beat,args=(application,))
    #c_beat.run(loglevel='DEBUG')
    pwork=Process(target=run_work,args=(application,))
    pbeat.start()
    pwork.start()
    #c_worker.run(loglevel='DEBUG')
    #c_worker.run(**config.CELERY_CONFIG)