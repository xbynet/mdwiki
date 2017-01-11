from app import config
from app.util.utilRedis import redis_decode_client as redis
import json
######################
#Menu
#######################


###在gunicorn指定多个work进程的情况下，跨模块共享修改G_SHARE会导致数据出现随机性不一致的情形。(这是应该由于进程间不共享内存所致。)故而采用redis来存储可变共享变量。
#
G_SHARE = \
        { \
            'title': config.APP_NAME, \
            'menus': [{'name': '标签', 'icon': 'tags', 'type': 0, 'link': '/pages/tag/list', 'active': ''}, \
                      {'name': '侧边栏', 'icon': 'tags', 'type': 0, 'link': '/sidebar/edit', 'active': ''}], \
            'sidebar': [] \
        }

def get_sidebar_key():
    return 'g:share:sidebar'

def set_sidebar(sidebar):
    key=get_sidebar_key()
    redis.set(key,json.dumps(sidebar))

def get_g_share():
    key=get_sidebar_key()
    G_SHARE['sidebar']=json.loads(redis.get(key),encoding='utf-8')
    return G_SHARE

##############################################################################################