import celery
from celery.schedules import crontab
from kombu import Queue
from datetime import timedelta
from celery.bin import beat,worker


celery_app = celery.Celery("proj",
             broker = "redis://127.0.0.1/2",
             include = ['proj.email_task']   #！！！！！
             )
 
celery_app.conf.update(
        CELERY_DEFAULT_QUEUE = 'default',
        CELERY_QUEUES = (Queue('hipri'),Queue('default')),
        #CELERY_ROUTES={
        #"proj.email_task.do_email":{'queue':'hipri'},
        #},
        CELERY_TIMEZONE = 'Asia/Shanghai',
        CELERYBEAT_SCHEDULE = {
            "do_email":{
                "task":"proj.email_task.do_email",
                "schedule":timedelta(seconds=5),
                "args":(),
                "options":{'queue':'default'}
                },
            "do_email_new":{
                "task":"proj.email_task.do_email_new",
                "schedule":timedelta(seconds=7),#crontab(minute="*/1"),
                "args":(),
                "options":{'queue':'hipri'}
                }
        }
    )
 
if __name__ == '__main__':
    pass
    #app.start()