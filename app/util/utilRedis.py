from app import config
import logging as log
from redis import StrictRedis,ConnectionPool
from redis.exceptions import ConnectionError
#不建议使用该decode_responses=True选项，因为当存在pickle序列化的值时，client.get(key)时会出现解码失败的错误UnicodeDecodeError
##如果仍要使用，在有ConnectionPool的情况下，也要把decode_responses=True传递给它，否则无效。
redis_pool=ConnectionPool(host=config.REDIS_HOST,port=config.REDIS_PORT,db=0)#decode_responses=True
redis_client=StrictRedis(connection_pool=redis_pool) #decode_responses=True,ignore_subscribe_messages=True

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

