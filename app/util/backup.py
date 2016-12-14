"""Summary
"""
import os
import sys, time
#sys.path.append('C:\\Users\\taojw\\Desktop\\pywork\\mdwiki')
import logging as log
import oss2
from datetime import datetime, timedelta
from itertools import islice
import tarfile

from app import config
from . import checkOS

class AliyunOSS(object):
    """Aliyun oss2 bakcup

    Attributes:
        auth (TYPE): Description
        bucket (TYPE): Description
    """
    oss2.defaults.connection_pool_size = 4

    # service=oss2.Service(auth,'http://oss-cn-shenzhen.aliyuncs.com')
    # bucketlist=oss2.BucketIterator(service)

    def __init__(self, api_key, secret_key, bucket_name, inner_endpoint=None, out_endpoint=None):
        """Summary

        Args:
            apiKey (TYPE): Description
            sercetKey (TYPE): Description
            bucket_name (TYPE): Description
            inner_endpoint (None, optional): Description
            out_endpoint (None, optional): Description
        """

        self.auth = oss2.Auth(api_key,
                              secret_key)
        self.bucket = oss2.Bucket(
            self.auth, inner_endpoint or out_endpoint, bucket_name, connect_timeout=600)

    def uploadFile(self, path):
        """simple file upload

        Args:
            path (TYPE): file abspath

        Returns:
            TYPE: <oss2.models.PutObjectResult> object you can use to get status or etag.
        """
        result = self.bucket.put_object_from_file(path.rsplit(
            os.sep, 1)[1], path, progress_callback=self.percentage)
        log.debug('httpStatus:{0}'.format(result.status))
        log.info('ETag:{0}'.format(result.etag))
        return result

    def resumableUpload(self, path):
        """断点续传上传

        Args:
            path (TYPE): file abspath

        Returns:
            TYPE: Description
        """
        part_size = os.path.getsize(path) if os.path.getsize(
            path) < 1024 * 1024 else os.path.getsize(path) // 10
        success = False
        retry = 10
        while not success and retry>0:
            retry -= 1
            try:
                oss2.resumable_upload(self.bucket, path.rsplit(os.sep, 1)[1], path, progress_callback=self.percentage,
                                      # store=oss2.ResumableStore(root='/tmp'),
                                      store=oss2.ResumableStore(root='/tmp' if checkOS()=='linux' else config.BASE_DIR),
                                      multipart_threshold=1024 * 1024,
                                      part_size=part_size,
                                      num_threads=4)
                success = True
                return True
            except oss2.exceptions.RequestError as e:
                log.warn('上传失败，即将进行重试')
                time.sleep(2)
                continue
        return False

    def listFiles(self):
        """list bucket files

        Returns:
            TYPE:dict for get name and size
        """
        # oss2.models.SimplifiedObjectInfo
        reslist = []
        for b in oss2.ObjectIterator(self.bucket):
            log.info("name:" + b.key + ",size:%.2fM" % (b.size / 1024 / 1024))
            reslist.append(dict(name=b.key, size="%.2fM" %
                                                 (b.size / 1024 / 1024)))
        return reslist

    def deleteFile(self, key):
        """delete file

        Args:
            key (TYPE): file key also is the name or the key list

        Returns:
            TYPE: Description
        """
        if isinstance(key,list):
            return self.bucket.batch_delete_objects(key)
        return self.bucket.delete_object(key)

    def getDownloadUrl(self, key):
        """get download url for file , valid in 1200s

        Args:
            key (TYPE): Description

        Returns:
            TYPE: the url for download
        """
        return self.bucket.sign_url('GET', key, 1200).replace('-internal','')  # 1200s

    def percentage(self, consumed_bytes, total_bytes):
        """upload progress record

        Args:
            consumed_bytes (TYPE): Description
            total_bytes (TYPE): Description

        Returns:
            TYPE: Description
        """
        print(str(consumed_bytes) + ":" + str(total_bytes))
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            #print('\r{0}% '.format(rate), end='')
            log.debug('\r{0}% '.format(rate))
            sys.stdout.flush()

    @staticmethod
    def getNow():
        """get now time str

        Returns:
            TYPE: Description
        """
        return datetime.now().strftime('%Y%m%d')


def tarzipData():
    """compress data to tar.gz
    
    Returns:
        TYPE: the compressed file path
    """
    dataPath=config.DATA_DIR
    base=os.path.abspath(os.path.join(dataPath,'..'))
    def excludePath(path):
        """Summary
        
        Args:
            path (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        for name in ['searchIndex']:
            if path.find(os.sep+name+os.sep)>0:
                return True
        return False
    backupPath=os.path.join(base,'backup')
    if not os.path.exists(backupPath):
        os.mkdir(backupPath)
    data=os.path.join(backupPath,'data%s.tar.gz' % datetime.now().strftime('%Y%m%d'))

    with tarfile.open(data,'w:gz') as f:
        f.add(dataPath,arcname='data',exclude=excludePath)
    
    #delete local files of prev 30days
    filelist=[backupPath+os.sep+'data'+(datetime.now()+timedelta(-i-30)).strftime('%Y%m%d')+'.tar.gz' for i in range(10)]
    for file in filelist:
        if os.path.exists(file):
            os.remove(file)

    return data



if __name__ == '__main__':
    

    oss=AliyunOSS(**config.oss)
    oss.resumableUpload(r'F:\workspace\nginx\nginx.exe')
    oss.listFiles()
    #print(oss.getDownloadUrl('222.zip'))
