import multiprocessing

bind = "127.0.0.1:4000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class='gevent'
proc_name = "mdwiki"
user = "www-data"
chdir='/opt/www/mdwiki'
#daemon=False
#group = "nginx"
loglevel = "info"
#errorlog = chdir+"/log/gunicorn/error.log"
#accesslog= chdir+"/log/gunicorn/access.log"
raw_env = [
   r'aliyun_api_key=value',
   r'aliyun_secret_key=value',
   r'MAIL_PASSWORD=value',
   r'SECRET_KEY=mysecretkey'
]
#ssl
#keyfile=
#certfile=
#ca_certs=