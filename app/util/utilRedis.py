from app import config
import logging as log
from redis import StrictRedis,ConnectionPool
from redis.exceptions import ConnectionError

redis_pool=ConnectionPool(host=config.REDIS_HOST,port=config.REDIS_PORT,db=0)
redis_client=StrictRedis(connection_pool=redis_pool,decode_responses=True) #ignore_subscribe_messages=True

def isValid():
    '''
    检测redis服务是否在运行
    '''
    try:
        redis_client.ping()
        return True
    except ConnectionError as e:
        log.warn('redis服务没有启动')
        return False  

