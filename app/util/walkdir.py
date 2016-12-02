import os
import sys
import shutil
import re

class WalkDir(object):
    """
    目录迭代工具类，
    构造器参数 
    -dirname-目录名
    -filters-过滤器函数元组,过滤器函数接收一个文件名参数，返回bool值
    -regexp-文件名匹配正则
    -exts-扩展名元组
    """
    def __init__(self,dirname='',filters=(),regexp='.*',exts=('',)):
        """Summary
        
        Args:
            dirname (str, optional): Description
            filters (tuple, optional): Description
            regexp (str, optional): Description
            exts (tuple, optional): Description
        """
        self.dirname=dirname
        self.dirlist=[]
        self.filelist=[]
        self.filters=filters
        self.regexp=regexp
        self.exts=exts

    def walk(self):
        self.__walkdir(self.dirname)
        return self.filelist,self.dirlist 
    def getFilelist(self):
       self.__walkdir(self.dirname)
       return self.filelist

    def __walkdir(self,dirname):
        """Summary
        
        Args:
            dirname (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        if not os.path.exists(dirname):
            return
        for path,dirs,files in os.walk(dirname):
            for name in files:
                if self.__filterPath(name) and self.__filterExt(name):
                    fullpath=os.path.join(path,name)
                    self.filelist.append(fullpath)  
            for dirfile in dirs:
                if dirfile=='.' or dirfile=='..':
                    continue
                if(self.__filterPath(dirfile)) and self.__filterExt(dirfile):
                    fullpath=os.path.join(path,dirfile)
                    self.dirlist.append(fullpath)
                    
    def __filterPath(self,name):
        """Summary
        
        Args:
            name (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        for filter in self.filters:
            if not filter(name):
                return False
        if re.match(self.regexp,name,re.I) is None:
            return False
        return True
    def __filterExt(self,name):
        """Summary
        
        Args:
            name (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        for ext in self.exts:
            if name.endswith(ext):
                return True
        return False
