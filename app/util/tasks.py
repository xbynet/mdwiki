import sys,os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
#import celery
#from celery.bin import worker as celery_worker
from app import config,app
from app.util import backup
from datetime import datetime,timedelta
from flask_mail import Message
from app.extensions import mail
import logging as log
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_jobstore('redis',jobs_key='mdwiki.jobs', run_times_key='mdwiki.run_times')

#坑啊，include必须填，没仔细看文档。
#celery_app=celery.Celery('app',include=['app.util.tasks'])

#celery_app.config_from_object(config.CELERY_CONFIG)

def sendMail(content):
    with app.app_context():
        msg=Message(content,recipients=['xby309778901@163.com'],
            body=content)
        mail.send(msg)

#@celery_app.task(name='tasks.backup')
@scheduler.scheduled_job('cron',minute=0,hour=4,id='backupDataTask')
def backupDataTask():
    #datapath='/opt/www/mdwiki/data'+datetime.now().strftime('%Y%m%d')+'.tar.gz'
    datapath=backup.tarzipData()

    oss=backup.AliyunOSS(**config.oss)
    isSuccess=oss.resumableUpload(datapath)
    
    #only retain recent 10 days file
    keylist=['data'+(datetime.now()+timedelta(-i-30)).strftime('%Y%m%d')+'.tar.gz' for i in range(10)]
    files=oss.listFiles()
    delKeylist=[key for key in keylist for file in files if key==file['name']]
    
    if len(delKeylist)>0:
        oss.deleteFile(delKeylist)
    
    status='成功' if isSuccess else '失败'
    msg='备份状态为:%s' % status
    sendMail(msg)

#@celery_app.task(name='tasks.backup')#name='tasks.backup'
def test():
    log.warn('aaaaaaaaaaaaaaaaaaaaaaaa')
    sendMail('您好，今天数据状态为:%s' % '成功')
    with open(r'C:\Users\taojw\Desktop\pywork\mdwiki\11.txt','a+') as f:
        f.write('1111')

#test.delay()

scheduler.start()