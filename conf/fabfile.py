from fabric.api import *
import os,sys
import tarfile
#$ fab -f fabfile.py -H localhost,remote host_type
def host_type():
    run('uname -s')

env.user='xxx'
env.hosts=['192.168.1.2']
env.password='123'
env.sudo_password='123'

srcPath='mdwiki'
distPath='dist'
distFile='dist'+os.sep+'mdwiki.tar.gz'
if not os.path.exists(distPath):
    os.mkdir(distPath)

def pack():
    def ecludefiles(path):
        for name in ['venv','node_modules','websrc','__pycache__','.git','.idea']:
            if path.find(os.sep+name)>0:
                return True
        return False

    if os.path.exists(distFile):
        os.remove(distFile)
    with tarfile.open(distFile,'w:gz') as f:
        f.add(srcPath,arcname='mdwiki',exclude=ecludefiles)

def deploy():
    #local pack dist file
    pack()
    
    remote_tmp='/tmp/mdwiki.tar.gz'

    sudo('rm -f %s' % remote_tmp)
    # upload dist file
    put(distFile,remote_tmp)
    #delete previous bak
    sudo('rm -rf /opt/www/mdwiki_bak')
    #stop app and bak now
    with settings(warn_only=True):
        sudo('supervisorctl stop all')
    sudo('mv /opt/www/mdwiki /opt/www/mdwiki_bak')

    sudo('tar -zxvf /tmp/mdwiki.tar.gz -C /opt/www/')
    with cd('/opt/www/'):
        #replace data dir
        sudo('rm -rf mdwiki/data')
        sudo('cp -R mdwiki_bak/data mdwiki/')

        sudo('chown -R nginx:nginx mdwiki')
    sudo('supervisorctl start all')

#in your local shell run 'fab deploy' command