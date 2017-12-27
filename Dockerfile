FROM ubuntu:16.04

WORKDIR /tmp
ENV SECRET_KEY=\xe0N\rl\x8f\xe3\x13\xa6\xdd\r\xea\xd1\x03\x9f+\x1f3\xa3\x18\x1eia\xa2\xbf \
    aliyun_api_key=your_key \
    aliyun_secret_key=your_secret_key \
    MAIL_NAME=your_163_mail \
    MAIL_PASSWORD=your_mail_pass
COPY ./conf/prod/nginx.conf /etc/nginx/conf.d/www.conf
COPY ./conf/prod/supervisor.conf /etc/supervisor/conf.d/mdwiki.conf
COPY . /opt/www/mdwiki/

RUN apt-get install -y gnupg \
 && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32 
COPY ./sources.list /etc/apt/
#&& sed -i s:/archive.ubuntu.com:/cn.archive.ubuntu.com:g /etc/apt/sources.list \
RUN apt-get update \
&& apt-get install -y less build-essential python-software-properties software-properties-common supervisor \
&& add-apt-repository -y ppa:nginx/stable \
# && add-apt-repository -y ppa:rwky/redis \
&& apt-get install -y curl wget nginx redis-server python3-pip libssl-dev libffi-dev python-dev python3-dev  \
    libevent-dev libssl-dev libffi-dev libsasl2-dev libpq-dev  libxml2-dev libxslt1-dev libldap2-dev \

&& mkdir ~/.pip \
&& echo '[global] \n\
index-url = https://pypi.douban.com/simple \n\
disable-pip-version-check = true      \n\
timeout = 120' > ~/.pip/pip.conf \

&& pip3 install -U pip --no-cache-dir\
&& pip3 install gunicorn --no-cache-dir\
&& pip3 install -r /opt/www/mdwiki/requirements.txt --no-cache-dir\
#&& wget https://github.com/xbynet/mdwiki/blob/master/conf/prod/nginx.conf \
#&& mv nginx.conf /etc/nginx/conf.d/www.conf \
#&& wget https://github.com/xbynet/mdwiki/blob/master/conf/prod/supervisor.conf \
#&& mv supervisor.conf /etc/supervisor/conf.d/mdwiki.conf \
&& apt-get remove wget -y \
&& apt-get clean && apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*  \
&& chown www-data:www-data -R /opt/www/mdwiki

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -fs http://localhost/ || exit 1
CMD service redis-server start && /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
EXPOSE 80 4000
