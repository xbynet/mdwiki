#!/bin/bash
#pip3 install Fabric3
#gunicorn -w 4 -b 127.0.0.1:4000 -k gevent -e key=value app:app 
#supervisorctl start all
#supervisorctl stop all
#
sudo dd if=/dev/zero of=/swapfile bs=1G count=2
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
#sudo swapon -s
##free -m
sudo vim /etc/fstab
#/swapfile       none    swap    sw      0       0 

sudo useradd -rm -s /bin/bash xby
sudo adduser xby sudo
sudo passwd xby

sudo apt-get install supervisor -y
sudo apt-get install vim nano -y
sudo apt-get install build-essential python-software-properties software-properties-common -y
sudo add-apt-repository ppa:nginx/stable 
sudo add-apt-repository -y ppa:rwky/redis
sudo apt-get update
sudo apt-get install nginx aria2 axel wget curl -y
sudo apt-get install -y redis-server
sudo apt-get install python3-pip -y
sudo apt-get install enca convmv libssl-dev libffi-dev python-dev python3-dev -y


#sudo apt-get install gunicorn -y
sudo apt-get install libevent-dev libssl-dev libffi-dev libsasl2-dev libpq-dev  libxml2-dev libxslt1-dev libldap2-dev  -y

#sudo pip3 install greenlet
#sudo pip3 install gevent


vim ~/.pip/pip.conf

#[global]
#index-url = https://pypi.douban.com/simple #豆瓣源，可以换成其他的源
#disable-pip-version-check = true          #取消pip版本检查，排除每次都报最新的pip
#timeout = 120


sudo pip3 install virtualenv
mkdir venv && cd venv 
virtualenv mdwiki
source mdwiki/bin/activate
pip3 install gunicorn
sudo vim  mdwiki/gunicorn.conf.py
sudo vim /etc/supervisor/conf.d/default.conf
sudo vim /etc/nginx/conf.d/default.conf

sudo vim /etc/rc.local
#/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
#pip3 install psutil selenium fabric paramiko gunicorn 


sudo update-rc.d nginx disable
