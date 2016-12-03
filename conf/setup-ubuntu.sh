#!/bin/bash
#sudo apt-get install python3-pip
#sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3-dev
sudo apt-get update -y
sudo apt-get install gunicorn -y
sudo apt-get install libevent
sudo pip3 install greenlet
sudo pip3 install gevent
sudo apt-get install supervisor
sudo pip3 install -r /opt/www/mdwiki/requirements.txt
#pip3 install Fabric3
#gunicorn -w 4 -b 127.0.0.1:4000 -k gevent -e key=value app:app 

#supervisorctl start all
#supervisorctl stop all