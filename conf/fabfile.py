from fabric.api import *
import os,sys
import tarfile
from contextlib import contextmanager
from fabric.contrib.files import exists


#$ fab -f fabfile.py -H localhost,remote host_type
def host_type():
    run('uname -s')

env.user= os.environ.get('USER','')
env.hosts= os.environ.get('HOST','').split(',')
env.password= os.environ.get('PASSWORD','')
env.sudo_password= os.environ.get('PASSWORD','')


shouldUpload= False if os.environ.get('upload','') else True

active='source /home/xby/venv/mdwiki/bin/activate'

srcPath=r'C:\Users\taojw\Desktop\pywork\mdwiki'
distPath=r'C:\Users\taojw\Desktop\pywork\mdwiki\dist'
distFile=distPath+os.sep+'mdwiki.tar.gz'

@contextmanager
def virtualenv():
    with prefix(active):
        yield


if not os.path.exists(distPath):
    os.mkdir(distPath)

def pack(excludes=[]):

    def ecludefiles(path):
        for name in ['venv','celerybeat-schedule','node_modules','websrc','__pycache__','.git','.idea','dist','.log']+excludes:
            if path.find(os.sep+name)>0:
                return True
        return False

    if os.path.exists(distFile):
        os.remove(distFile)
    with tarfile.open(distFile,'w:gz') as f:
        f.add(srcPath,arcname='mdwiki',exclude=ecludefiles)

def deploy():
    
    if exists('/opt/www/mdwiki/data',use_sudo=True):
        pack(excludes=['data'])
    else: 
        #local pack dist file
        pack()
    
    remote_tmp='/tmp/mdwiki.tar.gz'

    localsize=os.path.getsize(distFile)
    remotesize=0
    #check if should upload again if there is a same file
    if exists(remote_tmp) and shouldUpload:
        remotesize=int(run("stat -c '%s' {0}".format(remote_tmp)))
        print(str(localsize)+":"+str(remotesize))
    if localsize!=remotesize:
        sudo('rm -f %s' % remote_tmp)
        # upload dist file
        put(distFile,remote_tmp)
    if not exists('/opt/www'):
        sudo('mkdir /opt/www')
        sudo('chown www-data:www-data /opt/www')

    #stop app and bak now
    with settings(warn_only=True):
        #delete previous bak
        sudo('rm -rf /opt/www/mdwiki_bak')
        sudo('supervisorctl stop all')
        if exists('/opt/www/mdwiki'):
            sudo('mv /opt/www/mdwiki /opt/www/mdwiki_bak')

    sudo('tar -zxvf /tmp/mdwiki.tar.gz -C /opt/www/')

    with cd('/opt/www/'):
        #replace data dir
        if exists('mdwiki_bak/data'):
            sudo('rm -rf mdwiki/data')
            sudo('cp -R mdwiki_bak/data mdwiki/')
        if exists('mdwiki_bak/app.db'):
            sudo('rm -rf mdwiki/app.db')
            sudo('cp mdwiki_bak/app.db mdwiki/')

        sudo('chown -R www-data:www-data mdwiki')

        with virtualenv():
            run('pip3 install -r  mdwiki/requirements.txt')

    sudo('rm -f %s' % remote_tmp)
    sudo('supervisorctl start all')

#in your local shell run 'fab deploy' command