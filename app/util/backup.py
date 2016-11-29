"""Summary
"""
import os
import sys, time
import logging as log
import oss2
from datetime import datetime
from itertools import islice


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
        retry = 5
        while not success:
            retry -= 1
            try:
                oss2.resumable_upload(self.bucket, path.rsplit(os.sep, 1)[1], path, progress_callback=self.percentage,
                                      # store=oss2.ResumableStore(root='/tmp'),
                                      multipart_threshold=1024 * 1024,
                                      part_size=part_size,
                                      num_threads=4)
                success = True
            except oss2.exceptions.RequestError as e:
                log.warn('上传失败，即将进行重试')
                time.sleep(2)
                continue

    def listFiles(self):
        """list bucket files

        Returns:
            TYPE:dict for get name and size
        """
        # oss2.models.SimplifiedObjectInfo
        reslist = []
        for b in oss2.ObjectIterator(self.bucket):
            print("name:" + b.key + ",size:%.2fM" % (b.size / 1024 / 1024))
            reslist.append(dict(name=b.key, size="%.2fM" %
                                                 (b.size / 1024 / 1024)))
        return reslist

    def deleteFile(self, key):
        """delete file

        Args:
            key (TYPE): file key also is the name

        Returns:
            TYPE: Description
        """
        self.bucket.delete_object(key)

    def getDownloadUrl(self, key):
        """get download url for file , valid in 1200s

        Args:
            key (TYPE): Description

        Returns:
            TYPE: the url for download
        """
        return self.bucket.sign_url('GET', key, 1200)  # 1200s

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
            print('\r{0}% '.format(rate), end='')
            log.debug('\r{0}% '.format(rate))
            sys.stdout.flush()

    @staticmethod
    def getNow():
        """get now time str

        Returns:
            TYPE: Description
        """
        return datetime.now().strftime('%Y%m%d')


if __name__ == '__main__':
    alioss = AliyunOSS()
    alioss.resumableUpload(r'F:\workspace\nginx\222.zip')
    alioss.listFiles()
    print(alioss.getDownloadUrl('222.zip'))
