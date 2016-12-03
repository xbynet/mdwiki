import multiprocessing

bind = "127.0.0.1:4000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class='gevent'
proc_name = "mdwiki"
user = "nginx"
chdir='/opt/www/mdwiki'
#daemon=False
#group = "nginx"
loglevel = "info"
#errorlog = "/home/myproject/log/gunicorn.log"
#accesslog=
raw_env = [
   'aliyun_api_key=value',
   'aliyun_secret_key=value',
   'MAIL_PASSWORD=value',
   'SECRET_KEY=mysecretkey',
]
#ssl
#keyfile=
#certfile=
#ca_certs=